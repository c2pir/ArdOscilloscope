# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:12:57 2019
Serial thread to read and write with arduino board
@author: 46053149
"""
from PyQt5 import QtCore, QtGui, QtWidgets

import serial
import time
import serial.tools.list_ports


class ThreadSerial(QtCore.QThread):
    """objet thread """
    sData = QtCore.pyqtSignal(dict)
    sError = QtCore.pyqtSignal(list)
    
    def __init__(self, parent=None):
            QtCore.QThread.__init__(self,parent)
            self.ser = None
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
        """ Refresh alvailable ports list """
        self.ports = list(serial.tools.list_ports.comports())


    def connect(self,i):
        """ Try to connect at the port at index i in self.ports
        return True on success"""
        try:
            if i!=-1:
                self.disconnect()
                self.port_index = i
                self.ser = serial.Serial(self.ports[i].device,timeout=2.0)
                self.ser.baudrate = 115200 #38400 #19200 #250000
                print("INFO:Serial: connected to "+str(self.ports[i].device))
                return True
            error_msg = "ERROR:Serial: no ports found"
        except:
            if (len(self.ports)!=0):
                error_msg = "ERROR:Serial: connection failed"
            else:
                error_msg = "ERROR:Serial: no ports found"
        print(error_msg)
        self.sError.emit(["","Not able to connect.",error_msg])
        return False


    def set_baudrate(self,baudrate):
        if self.ser is not None:
            self.ser.baudrate = baudrate
        else:
            print("WARNING:Serial: not able to set the buadrate")


    def disconnect(self):
        if self.ser is not None:    
            print("INFO: disconnect")
            self.ser.close()
            self.ser = None


    def send(self,msg):
        """Add msg to the queue"""
        try:
            if self.mutexCmd.tryLock(100):
                self.cmd.append(msg)
                self.mutexCmd.unlock()
                #print("ADD TO QUEUE: {}".format(msg))
            else:
                print("WARN: cmd not added to queue")
        except Exception as e:
            print("ERROR:Serial:send:",e)
            self.ConnexionError.emit(True)
#            try:
#                self.ser.flushInput()
#                self.ser.write(str(msg))
#            except:
#                pass


    def sendAuto(self):
        """Send first message in the queue"""
        if (self.ser is not None):
            if len(self.cmd)>0:
                try:
                    # TODO gestion python 2.0 (str) ou 3.0 (encode)
                    cmd = self.cmd[0] + "\n"
                    self.ser.write(cmd.encode())
                    self.t_TX = time.time()
                    if self.mutexCmd.tryLock(100):
                        del self.cmd[0]
                        self.mutexCmd.unlock()
                    else:
                        print("WARN: cmd not send")
                    print(self.t_TX, cmd[:-1])
                except Exception as e:
                    print("ERROR:Serial:sendAuto",e)


    def read(self):
        """Read one line"""
        if self.ser is not None:
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
                        print("{} {} dt={}".format(time.time(), self.msg[:-1], dt))
                    
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
