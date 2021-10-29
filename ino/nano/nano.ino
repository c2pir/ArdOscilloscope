const int nD = 10;
const int nA = 8;
int modeD[nD];
int modeA[nA];
int pinD[nD]; 
int pinA[nA] = {A0, A1, A2, A3, A4, A5, A6, A7};
bool valueD[nD];
int valueA[nA];
String msg;

int cpt = 0;
const int getCpt = 10;

void init_pins_variables(){
  for (int i=0; i<nD; i++){
    pinD[i] = i+2;
    valueD[i] = LOW;
    modeD[i] = 0;
  }
  for (int i=0; i<nA; i++){
    valueA[i] = 0;
    modeA[i] = 0;
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  init_pins_variables();
}

void loop() {
  // put your main code here, to run repeatedly:

  // read order from the computer
  if (Serial.available()) {
    msg = Serial.readString(); // read the incoming data as string

    // SET PIN MODE
    //par:D:2:2
    if (msg.substring(0,3)=="par") {
      String pinType = getValue(msg,':',1);
      int pinId = getValue(msg,':',2).toInt();
      int piMode = getValue(msg,':',3).toInt();

      bool mode;
      if (piMode==1){
          mode = INPUT;
      }
      if (piMode==2){
          mode = OUTPUT;
      }
      
      if ((pinType=="D") && (piMode!=0)){
          pinMode(pinD[pinId], mode);
          modeD[pinId] = piMode;
          Serial.println("ACK:"+msg);
      }

      if ((pinType=="A") && (piMode!=0)){
          //pinMode(pinA[pinId], INPUT_PULLUP);
          modeA[pinId] = piMode;
          Serial.println("ACK:"+msg);
      }
      
    }

    // SET PIN VALUE
    // set:D2_1:D3_0: ...
    if (msg.substring(0,3)=="set") {
      String couples = msg.substring(4);

      int start = 0;
      for (int i=0; i< couples.length(); i++) {
        if (couples.charAt(i) == ':'){
          String c = couples.substring(start, i);

          int j = c.indexOf('_');
          String pinType = c.substring(0, 1);
          int pinId = c.substring(1, j).toInt();
          int pinValue = c.substring(j+1).toInt();

          if (pinType=="D"){
            valueD[pinId] = pinValue;
            Serial.println("ACK:"+msg);
          }
          start = i+1;
          
        }
      }
    }
  }

  // READ LOOPS
  for (int i=0; i<nD; i++){
    if (modeD[i]==1){
      valueD[i] = (int)(digitalRead(pinD[i]));
    }
  }
  for (int i=0; i<nA; i++){
    if (modeA[i]==1){
      valueA[i] = analogRead(pinA[i]);
    }
  }

  // WRITE LOOP
  for (int i=0; i<nD; i++){
    if (modeD[i]==2){
      digitalWrite(pinD[i], valueD[i]);
    }
  }

  // GET
  cpt += 1;
  if (cpt>=getCpt){
    Serial.print("GET");
    for (int i=0; i<nD; i++){
      Serial.print(":"+String(valueD[i]));
    }
    for (int i=0; i<nA; i++){
      Serial.print(":"+String(valueA[i]));
    }
    Serial.println(":");
    cpt = 0;  
  }
  
}

String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}
