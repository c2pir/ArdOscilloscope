# -*- coding: utf-8 -*-
"""
"""
import time

def refresh_port_list():
    # TODO
    return []

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

def start_recording(cls, nb_points = 1000, show = False):
    """Start records
    nb_points: number of points before looping data recording
    show: if True UI will display data in 'real time'
    """
    cls.thRecorder.nbPoints = nb_points
    cls.thRecorder.update_displayer = show
    cls.thRecorder.flush()
    if show and cls.centralwidget.figure.mpl_toolbar.pbsPlayPause.state: 
        cls.centralwidget.figure.mpl_toolbar.pbsPlayPause.clicked.emit(False)

def stop_recording(cls):
    """ """
    cls.thRecorder.update_displayer = True
    
    if (not cls.centralwidget.figure.mpl_toolbar.pbsPlayPause.state): 
        cls.centralwidget.figure.mpl_toolbar.pbsPlayPause.clicked.emit(False)
    else:
        cls.thRecorder.show()

def configure_pin(cls, name, mode=0, watch=True):
    """Configure a pin
    name: pin name (as shown in the UI
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

def set_pin(cls, name, value):
    """Set a pin in write mode to the given value
    name: pin name (as shown in the UI
    value: 
    """
    row = 0
    for conf in cls.centralwidget.flwPins.json:
        if conf["name"]==name:
            if ("D" in conf["type"]) and ("I" in conf["type"]):
                cls.thSerial.send("set:D{}_{}:".format(conf["id"], value))
            # TODO analog write
            # TODO PWM
        row+=1

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
