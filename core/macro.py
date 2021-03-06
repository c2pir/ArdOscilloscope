# -*- coding: utf-8 -*-
"""
Functions usable in a macro

    cls argument allow to have access to all UI functionalities
    it is given in your custom macro with 'def run(cls):' (the function containing your macro)
"""
import time


def refresh_port_list(cls):
    """Refresh alvailable port list
    return: alvailable ports list"""
    cls.refresh()
    return cls.thSerial.ports


def connect(cls, port_name):
    """Try to connect to a given port
    return True on success"""
    # disconnect if a connection is already established
    if is_connected(cls):
        cls.centralwidget.fpbsConnect.clicked.emit(True)
        time.sleep(1.0)
    
    # try to find port
    i = 0
    for port in cls.thSerial.ports:
        if port_name in str(port):
            cls.centralwidget.fcbPort.cb.setCurrentIndex(i)
            cls.centralwidget.fpbsConnect.clicked.emit(True) 
            time.sleep(2.0)
            return True
        i+=1
    
    return False


def is_connected(cls):
    """Check if communication is established
    return: True if serial port is connected"""
    if cls.thSerial.ser is None:
        return False
    else:
        return True


def start_recording(cls, nb_points = 1000):
    """Start records
    nb_points: number of points before looping data recording
    """
    cls.thRecorder.nbPoints = nb_points
    cls.thRecorder.do_record = True
    cls.thRecorder.flush()


def stop_recording(cls):
    """Stop records"""
    cls.thRecorder.do_record = False


def show_data(cls):
    """Display recorded data on UI"""
    cls.thRecorder.update_displayer = True
    cls.thRecorder.show()


def configure_pin(cls, name, mode=0, watch=True):
    """Configure a pin
    name: pin name (as shown in the UI)
    mode: index of the corresponding UI combo box
    watch: if true pin values will be saved
    """
    row = 0
    for conf in cls.centralwidget.flwPins.json:
        if conf["name"]==name:
            cls.centralwidget.flwPins.cellWidget(row,0).cb.setChecked(watch) #stateChanged.emit()
            if cls.centralwidget.flwPins.cellWidget(row,2).currentIndex() != mode:
                cls.centralwidget.flwPins.cellWidget(row,2).setCurrentIndex(mode)
            else:
                cls.centralwidget.flwPins.cellWidget(row,2).currentIndexChanged.emit(mode)
            time.sleep(0.2)
        row +=1
    pass


def set_pin(cls, names, values):
    """Set a pin in write mode to the given value
    names: list of pins names (as shown in the UI)
    values: list of desired pin values
    """
    cmd = "set:"
    
    for i in range(len(names)):
        row = 0
        for conf in cls.centralwidget.flwPins.json:
            if conf["name"]==names[i]:
                # digital write
                if ("D" in conf["type"]) and ("I" in conf["type"]) and (conf["mode"]==2):
                    cmd += "D{}_{}:".format(conf["id"], values[i])
                # analog write (PWM)
                if conf["mode"]==3:
                    cmd += "A{}_{}:".format(conf["id"], values[i])
                break
            row+=1
    cls.thSerial.send(cmd)


def get_pin(cls, names):
    """Get pins actual values by names
    names: list of pins names (as shown in the UI)"""
    res = []
    for i in range(len(names)):
        row = 0
        for conf in cls.centralwidget.flwPins.json:
            if conf["name"]==names[i]:
                try:
                    v = cls.thRecorder.current_pins_values[row]
                    res.append(v)
                except Exception as e:
                    print("ERROR:MACRO:get_pin",e)
            row += 1
    return res


def save_data_as_csv(cls, file_name, separator=";"):
    """Save recordeed data as csv (you need to call start_recording before)
    file_name: relative path where the file will be created
    separator: csv character for cell separator
    """
    t = cls.thRecorder.time
    dataA, dataD = cls.thRecorder.filter_data()
    
    csv = "time;"
    # headers
    for key in dataA:
        csv+=key+separator
    for key in dataD:
        csv+=key+separator
    csv += "\n"
    
    # datas
    for i in range(cls.thRecorder.nbPoints):
        if i<len(t):
            csv += str(t[i])+separator
        for key in dataA:
            if i<len(dataA[key]):
                csv += str(dataA[key][i])+separator
        for key in dataD:
            if i<len(dataD[key]):
                csv += str(dataD[key][i])+separator
        csv += "\n"
    
    f = open(file_name, "w")
    f.write(csv)
    f.close()


def add_trigger(cls, pin_name, condition, method):
    """Attach a pin condition to a method
    pin_name: pin name of the pin value used as input of the condition
    condition: function that return a boolean (ex: 'lambda x: x==1')
    method: callback when condition is true (method must take one argument)
    """
    row = 0
    for conf in cls.centralwidget.flwPins.json:
        if conf["name"]==pin_name:
            break
        row += 1
    
    d = {"index": row, "condition": condition, "method": method}
    if d not in cls.callbacks: 
        cls.callbacks.append(d)


def remove_triggers(cls):
    """Remove all triggers added"""
    cls.callbacks = []