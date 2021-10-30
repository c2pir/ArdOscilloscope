# -*- coding: utf-8 -*-
"""
Created on Tue Mar 07 08:22:34 2017
@author: arnaud1
"""

import sys
import matplotlib
from PyQt5 import QtCore, QtGui, QtWidgets
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure
import numpy as np

from .Fields import PBSField


class CustomNavigationToolbar( NavigationToolbar ):
    picked=QtCore.pyqtSignal(int,name='picked')

    def __init__(self, canvas, parent):
        NavigationToolbar.__init__(self,canvas,parent,True) # False to not show coordinates

        self.pbsPlayPause = PBSField(["img/play.ico", "img/pause.png"])
        self.addWidget(self.pbsPlayPause)
        
        self.clearButtons=[]
        
        
        # Search through existing buttons
        nextB=None
        not_in = ('Subplots','Customize') # ('Subplots','Customize','Home','Pan','Zoom','Back','Forward','Save')
        
        for c in self.findChildren(QtWidgets.QToolButton):
            if nextB is None:
                nextB=c
            # Don't want to see subplots and customize
            if str(c.text()) in not_in:
                c.defaultAction().setVisible(False)
                continue
            # Need to keep track of pan and zoom buttons
            # Also grab toggled event to clear checked status of picker button
            if str(c.text()) in ('Pan','Zoom'):
                self.clearButtons.append(c)
                nextB=None
        
    def pickerToggled(self, checked):
        if checked:            
            if self._active == "PAN":
                self.pan()
            elif self._active == "ZOOM":
                self.zoom()
            self.set_message('Reject/use observation')

class SFigure(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        
        # Create the mpl Figure and FigCanvas objects. 5x4 inches, 100 dots-per-inch
        self.dpi = 100#20
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.fig.subplots_adjust(left=0.10, bottom=0.10, right=0.98, top=0.95)
        
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
#        self.canvas.mpl_connect('button_release_event',self.onRelease)
#        self.canvas.mpl_connect('motion_notify_event',self.onMouseMove)
        self.canvas.mpl_connect('button_press_event',self.onPress)
        
        self.axeD = self.fig.add_subplot(211)
        self.axeA = self.fig.add_subplot(212)
        self.nbPoints = 500
                
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = CustomNavigationToolbar(self.canvas, self)
        
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.mpl_toolbar)
        vbox.addWidget(self.canvas)
        self.setLayout(vbox)   

    
    def onPress(self,event):
        pass
    
    def onMouseMove(self,event):
        pass
    
    def onRelease(self,event):
        pass
    
    def draw(self, time, dataA, dataD):
        self.axeD.clear()
        self.axeA.clear()
        for key in dataD:
            self.axeD.plot(dataD[key], label=key)
        
        for key in dataA:
            self.axeA.plot(dataA[key], label=key)
        
        self.axeD.legend()
        self.axeA.legend()
        self.axeA.grid()
        #self.axe.set_aspect('equal')
        self.canvas.draw()
    

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = SFigure()
    form.show()
    app.exec_()
    
if __name__ == "__main__":
    main()
