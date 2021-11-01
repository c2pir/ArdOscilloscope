# -*- coding: utf-8 -*-
"""
"""
import time

def refresh_port_list():
    # TODO
    return []

def connect(port):
    # TODO
    return True

def start_recording(cls, loop = False, nb_points = 1000):
    cls.thRecorder.nbPoints = nb_points
    cls.thRecorder.doLoop = loop
    if cls.centralwidget.figure.mpl_toolbar.pbsPlayPause.state: 
        cls.centralwidget.figure.mpl_toolbar.pbsPlayPause.clicked.emit(False)

def stop_recording(cls):
    cls.thRecorder.doLoop = True
    if not cls.centralwidget.figure.mpl_toolbar.pbsPlayPause.state: 
        cls.centralwidget.figure.mpl_toolbar.pbsPlayPause.clicked.emit(False)

def save_data(file_name):
    #TODO
    pass

def configure_pin(cls, name, mode=0, watch=True):
    row = 0
    for conf in cls.centralwidget.flwPins.json:
        if conf["name"]==name:
            cls.centralwidget.flwPins.cellWidget(row,0).cb.setChecked(watch) #stateChanged.emit()
            cls.centralwidget.flwPins.cellWidget(row,2).setCurrentIndex(mode)
            time.sleep(0.2)
        row +=1
    pass

def set_pin(cls, name, value):
    row = 0
    for conf in cls.centralwidget.flwPins.json:
        if conf["name"]==name:
            if ("D" in conf["type"]) and ("I" in conf["type"]):
                cls.thSerial.send("set:D{}_{}:".format(conf["id"], value))
        row+=1

def save_data_as_csv(cls, file_name, separator=";"):
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
