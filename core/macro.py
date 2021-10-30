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

