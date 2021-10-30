# -*- coding: utf-8 -*-
"""
"""
from PyQt5 import QtCore, QtGui, QtWidgets
import time

class Recorder(QtCore.QThread):

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self,parent)
        
        self.nbPoints = 1000
        self.stop = False
        self.displayer = None
        self.updateFrequency = 2.0 #Hz
        self.last_time = time.time()
        
        
    def connect_to_pins(self, pins):
        self.pins = pins
        self.datas = [[] for i in range(len(self.pins.json))]
        self.time = []
        self.current_index = 0

    def receiveData(self, dico):
        try:
            data = dico["list"]
            
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
        except Exception as e:
            print("ERROR:Recorder:receiveData",e)
            
    def filter_data(self):
        dataA, dataD = {}, {}
        for i in range(len(self.pins.json)):
            conf = self.pins.json[i]
            if conf["type"].startswith("D") and conf["watch"]==2:
                dataD[conf["name"]] = self.datas[i]
            if conf["type"].startswith("A") and conf["watch"]==2:
                dataA[conf["name"]] = self.datas[i]
        return dataA, dataD
            
    def run(self):
        while not self.stop:
            # TODO refresh plot
            if time.time()-self.last_time >= 1.0/self.updateFrequency:
                self.last_time = time.time()
                if self.displayer is not None:
                    dataA, dataD = self.filter_data()
                    self.displayer.draw(self.time, dataA, dataD)
                time.sleep(0.2)