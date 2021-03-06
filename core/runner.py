# -*- coding: utf-8 -*-
"""
Python code runner module
"""
from PyQt5 import QtCore, QtGui, QtWidgets
import time

class Runner(QtCore.QThread):
    """Thread to run a macro"""
    sEnd = QtCore.pyqtSignal()          # signal send when macro is finished
    sError = QtCore.pyqtSignal(list)    # signal send to display error
    
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self,parent)
        
        # VARIABLES
        self.ui = parent
        self.name = None
        
            
    def run(self):
        """Import and run a custom macro"""
        try:
            module = __import__("macros", fromlist=[self.name])
            my_macro =  getattr(module, self.name)
            print(self.name, my_macro)
            my_macro.run(self.ui)
        except Exception as e:
            self.sError.emit(["","Macro failed.",str(e)])
        
        # TODO unload module
        #setattr(module, self.name, None)
        
        # set recording parameters as usual
        self.ui.thRecorder.do_record = True
        self.ui.thRecorder.nbPoints = 1000
        self.ui.thRecorder.flush()
        
        print("END OF MACRO")
        self.sEnd.emit()