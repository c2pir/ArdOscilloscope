# -*- coding: utf-8 -*-
"""
Data recorder module
"""
from PyQt5 import QtCore, QtGui, QtWidgets
import time
import numpy as np

class Recorder(QtCore.QThread):
    """Thread to store data from the board"""
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self,parent)
        
        # VARIABLES
        self.nbPoints = 1000                # number of points before recording start to loop
        self.stop = False                   # boolean to leave the thread
        self.displayer = None               # UI object used to display data
        self.update_displayer = True        # boolean to enable periodic display update
        self.do_record = True               # boolean to enable data recording
        self.current_pins_values = []       # last received pins values
        self.update_frequency = 2.0         # frequency of display update (Hz)
        self.last_time = time.time()
        self.mutexData = QtCore.QMutex()


    def connect_to_pins(self, pins):
        """Initialize datas from pins"""
        self.pins = pins
        self.datas = [[] for i in range(len(self.pins.json))]
        self.time = []
        self.current_index = 0


    def flush(self):
        """Clear datas list"""
        if self.mutexData.tryLock(10):
            for i in range(len(self.datas)):
                self.datas[i] = []
            self.time = []
            self.current_index = 0
            self.mutexData.unlock()
            return True
        return False

    def receiveData(self, dico):
        """Callback to store data from arduino board"""
        try:
            data = dico["list"]
            
            # save last reception
            self.current_pins_values = [int(v) for v in data]
            
            # save received data
            if self.do_record:
                if self.mutexData.tryLock(10):
                    
                    if len(self.time)==self.nbPoints:
                        self.time[self.current_index] = dico["timestamp"]
                    else:
                        self.time.append(dico["timestamp"])
                    
                    
                    for i in range(len(data)):
                        if i>=len(self.datas):
                            break
                        
                        if len(self.datas[i])==self.nbPoints:
                            self.datas[i][self.current_index] = int(data[i])
                        else:
                            self.datas[i].append(int(data[i]))
                            
                    self.current_index = (self.current_index+1)%self.nbPoints
                    
                    self.mutexData.unlock()
                    return True
        except Exception as e:
            print("ERROR:Recorder:receiveData",e)
        return False


    def filter_data(self):
        """ Filter data to show 
        return: dataA, dataD tables of analogic and digital values"""
        dataA, dataD = {}, {}
        if self.mutexData.tryLock(200):
            for i in range(len(self.pins.json)):
                conf = self.pins.json[i]
                if conf["type"].startswith("D") and conf["watch"]==2:
                    val = np.array(self.datas[i], dtype=float)
                    if conf["mode"]==3: # PWM display
                        val *= 1.0/255.0
                    dataD[conf["name"]] = list(val)
                if conf["type"].startswith("A") and conf["watch"]==2:
                    dataA[conf["name"]] = self.datas[i]
            self.mutexData.unlock()
        return dataA, dataD


    def show(self):
        """Method to display selected data on the grapher"""
        if self.update_displayer:
            dataA, dataD = self.filter_data()
            self.displayer.draw(self.time, dataA, dataD)


    def run(self):
        """Thread loop to refresh grapher"""
        while not self.stop:
            if time.time()-self.last_time >= 1.0/self.update_frequency:
                self.last_time = time.time()
                if self.displayer is not None:
                    self.show()
                # if data reception is blocked, increase this sleep time
                time.sleep(0.6)