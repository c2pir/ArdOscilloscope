# -*- coding: utf-8 -*-
"""
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from ui.UIConf import UIConf
from core.com import ThreadSerial
from core.recorder import Recorder
import json


import os
current_directory=os.getcwd()


class Ui_Main(QtWidgets.QMainWindow):
    """ Main window object """
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        # VARIABLES
        self.open_file_name = "conf/Arduino nano.json"
        self.result = None
        self.thSerial = ThreadSerial()
        self.thRecorder = Recorder()
        f = open(self.open_file_name ,"r")
        txt = f.read()
        f.close()
        d = eval(txt)
        
        ## GUI
        self.resize(1353, 812)
        
        self.setWindowTitle("ArdOscil")
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/monitor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.centralwidget = UIConf(d)
        self.setCentralWidget(self.centralwidget)
        
        
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1353, 26))
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuComplements = QtWidgets.QMenu("Complements",self.menubar)
        self.setMenuBar(self.menubar)
        self.actionShow = QtWidgets.QAction(self)
        self.actionNew = QtWidgets.QAction(self)
        self.actionOpen = QtWidgets.QAction(self)
        self.actionSave = QtWidgets.QAction(self)
        self.actionSave_as = QtWidgets.QAction(self)
        
        #self.actionSee_tt_validity = QtWidgets.QAction("See training table validity",self)
        
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        
        #self.menuComplements.addAction(self.actionSee_tt_validity)

        self.menubar.addAction(self.menuFile.menuAction())
        #self.menubar.addAction(self.menuComplements.menuAction())
        
        
        
        self.menuFile.setTitle("File")
        self.actionOpen.setText("Open")
        self.actionSave.setText("Save")
        self.actionSave_as.setText("Save as...")

        
        
        # BINDINGS
        self.actionOpen.triggered.connect(self.open_)
        self.actionSave_as.triggered.connect(self.saveAs)
        self.actionSave.triggered.connect(self.save)
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionSave.setShortcut("Ctrl+S")
        self.centralwidget.flwPins.sChangeMode.connect(self.changeMode)
        self.centralwidget.flwPins.sChangeWatch.connect(self.changeWatch)
        self.centralwidget.fpbRefresh.clicked.connect(self.refresh)
        self.centralwidget.fpbConnect.clicked.connect(self.connect)
        self.centralwidget.fpbSend.clicked.connect(self.send)
        self.centralwidget.figure.mpl_toolbar.pbsPlayPause.method = self.playPause
        self.thSerial.sData.connect(self.thRecorder.receiveData)
        
        self.thRecorder.connect_to_pins(self.centralwidget.flwPins)
        self.thRecorder.displayer = self.centralwidget.figure
        
        
    def connect(self):
        ind = self.centralwidget.fcbPort.cb.currentIndex()
        print(ind)
        self.thSerial.connect(ind)
        self.thSerial.start()
        self.thRecorder.start()

    def playPause(self, play):
        if play:
            self.thRecorder.stop = False
            self.thRecorder.start()
        else:
            self.thRecorder.stop = True
        

    def refresh(self):
        self.thSerial.refresh()
        self.centralwidget.fcbPort.load(self.thSerial.ports)

    def send(self):
        cmd = self.centralwidget.leCmd.text()
        self.thSerial.send(cmd)

    def changeMode(self, conf):
        #print(conf)
        cmd = "par:{}:{}:{}".format(conf["type"][0],
                                    conf["id"],
                                    conf["mode"])
        self.thSerial.send(cmd)

    def changeWatch(self, conf):
        print(conf)
    
    
    def save(self):
        if self.open_file_name==-1:
            self.saveAs()
        else:
            txt = json.dumps(self.centralwidget.flwPins.json, indent=4)
            file_=open(self.open_file_name,'w')
            file_.write(txt)
            file_.close()
            print("File saved")
    
    def saveAs(self):
        f = QtWidgets.QFileDialog()
        f.setMaximumSize(700,400)
        f.setWindowModality(QtCore.Qt.WindowModal)
        filename = f.getSaveFileName(self,"Save as...",
                                     current_directory+"/conf",
                                     filter="Pin config (*.json)")
        if type(filename)!=str:
            filename=filename[0]
        else:
            filename=str(filename)
        if filename != "":
            txt = json.dumps(self.centralwidget.flwPins.json, indent=4)
            print(txt)
            file_=open(filename,'w')
            file_.write(txt)
            file_.close()
            self.open_file_name = filename

    def open_(self):
        f = QtWidgets.QFileDialog()
        f.setMaximumSize(700,400)
        f.setWindowModality(QtCore.Qt.WindowModal)
        filename = f.getOpenFileName(self, 'Open conf',
                                     current_directory+"/conf",
                                     filter="Pin config (*.json)")
        if type(filename)!=str:
            filename=filename[0]
        else:
            filename=str(filename)
        if filename != "":
            file_=open(filename,'r')
            JSON=file_.read()
            file_.close()
            d = eval(JSON)
            self.centralwidget.flwPins.load(d)
            self.open_file_name = filename
    

    def closeEvent(self, event):
        self.thSerial.stop = True
        self.thRecorder.stop = True
        self.thSerial.disconnect()
        event.accept()
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv) #
    icon = QtGui.QIcon()
    icon.addFile("img/Brain-Icon.png",QtCore.QSize(24,24))
    app.setWindowIcon(icon)
    MainWindow = Ui_Main()
    MainWindow.show()
    #MainWindow.showMaximized()
    
    sys.exit(app.exec_())

