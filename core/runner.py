# -*- coding: utf-8 -*-
"""
"""
from PyQt5 import QtCore, QtGui, QtWidgets
import time

class Runner(QtCore.QThread):
    sEnd = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self,parent)
        
        self.ui = parent
        self.name = None
        
            
    def run(self):
        try:
            module = __import__("macros", fromlist=[self.name])
            my_macro =  getattr(module, self.name)
            print(self.name, my_macro)
            my_macro.run(self.ui)
        except Exception as e:
            print(e)
        print("END OF MACRO")
        self.sEnd.emit()