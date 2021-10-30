# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:12:57 2019
@author: 46053149
"""
from PyQt5 import QtCore, QtGui, QtWidgets

import serial
import time
import serial.tools.list_ports


class ThreadSerial(QtCore.QThread):
    """objet thread """
    sData = QtCore.pyqtSignal(dict)
    ConnexionError = QtCore.pyqtSignal(bool)
 
    def __init__(self, parent=None):
            QtCore.QThread.__init__(self,parent)
            self.ser = -1
            self.stop = False
            self.msg = ""

            self.mutexCmd = QtCore.QMutex()
            self.cmd = []

            
            self.t_TX = time.time()
            self.t_RX = time.time()
            self.samplingFrequency = 1000 # Hz
            self.port_index = -1

            self.refresh()

    def refresh(self):
        self.ports = list(serial.tools.list_ports.comports())
        print(self.ports)
    
    def connect(self,i):
        try:
            if i!=-1:
                self.disconnect()
                self.port_index = i
                self.ser = serial.Serial(self.ports[i].device,timeout=2.0)
                self.ser.baudrate = 19200 #250000
                print("INFO:Serial: connected to "+str(self.ports[i].device))
        except:
            if (len(self.ports)!=0):
                print("ERROR:Serial: connection failed")
            else:
                print("ERROR:Serial: no ports found")
    
    def set_baudrate(self,baudrate):
        if self.ser!=-1:
            self.ser.baudrate = baudrate
        else:
            print("WARNING:Serial: not able to set the buadrate")
    
    def disconnect(self):
        if self.ser!=-1:    
            print("INFO: disconnect")
            self.ser.close()
            self.ser = -1
    
    def send(self,msg):
        try:
            if self.mutexCmd.tryLock(10):
                self.cmd.append(msg)
                self.mutexCmd.unlock()
            
        except Exception as e:
            print("ERROR:Serial:send:",e)
            self.ConnexionError.emit(True)
#            try:
#                self.ser.flushInput()
#                self.ser.write(str(msg))
#            except:
#                pass
    
    def sendAuto(self):
        if (self.ser!=-1):
            if len(self.cmd)>0:
                try:
                    # TODO gestion python 2.0 (str) ou 3.0 (encode)
                    self.ser.write(self.cmd[0].encode())
                    self.t_TX = time.time()
                    print(self.t_TX, self.cmd[0])
                    if self.mutexCmd.tryLock(10):
                        del self.cmd[0]
                        self.mutexCmd.unlock()
                    
                except Exception as e:
                    print("ERROR:Serial:sendAuto",e)
                    print(e)
            
    def read(self):
        if self.ser!=-1:
            if self.ser.isOpen():
                try:
                    # TODO gestion python 2.0 (str) ou 3.0 (decode("utf-8"))
                    self.msg = self.ser.readline().decode("utf-8")
                    #self.ser.flushInput()
                    self.msg = self.msg.replace('\r\n','')
                    if "GET" in self.msg: #.startswith("GET"):
                        self.sData.emit({
                                        "timestamp": time.time(),
                                        "list": self.msg.split(":")[1:-1]
                                        })
                    if False: # perfo debug
                        print("{} {} dt={}".format(time.time(), self.msg, time.time()-self.t_RX))
                        self.t_RX = time.time()
                    
                    if self.msg.startswith("ACK"):
                        dt = time.time() - self.t_TX
                        print("{} {} dt={}".format(time.time(), self.msg, dt))

                except Exception as e:
                    print("ERROR:Serial:read",e)
        else:
            #self.connect(self.port_index)
            #time.sleep(0.5)
            pass
        
            
    def run(self):
        while not self.stop:
            self.read()
            self.sendAuto()
            
            #if (time.time()-self.t0>1.0/self.samplingFrequency):
            #    self.t0=time.time()
