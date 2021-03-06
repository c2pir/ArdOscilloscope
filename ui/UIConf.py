# -*- coding: utf-8 -*-
"""
Main window centralwidget content
"""
from PyQt5 import QtCore, QtGui, QtWidgets

from .Fields import CBField, PBField, PBSField
from .PinConf import PinTable
from .Plot import SFigure

class UIConf(QtWidgets.QWidget):
    """ """
    def __init__(self, _json, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        vl = QtWidgets.QVBoxLayout(self)
        vl.setContentsMargins(6, 6, 6, 6)

        hl0 = QtWidgets.QHBoxLayout()        
        self.fcbPort = CBField("Port")
        self.fcbPort.cb.setMinimumWidth(200)
        self.fpbRefresh = PBField("img/refresh.png",tool_tip="refresh ports list")
        self.fpbsConnect = PBSField(["img/connect.png","img/disconnect.png"], ["connect","disconnect"])
        self.leCmd = QtWidgets.QLineEdit()
        self.leCmd.setPlaceholderText("set:D2_1:D3_0:")
        self.leCmd.setToolTip("direct serial command for arduino board")
        self.fpbSend = PBField("img/send.png",tool_tip="send command")
        spacerItem = QtWidgets.QSpacerItem(20, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.fpbsMacro = PBSField(["img/led-red-on.png","img/green-led-on.png"], ["run macro","stop current macro"])
        
        hl0.addWidget(self.fcbPort)
        hl0.addWidget(self.fpbRefresh)
        hl0.addWidget(self.fpbsConnect)
        hl0.addWidget(self.leCmd)
        hl0.addWidget(self.fpbSend)
        hl0.addWidget(self.fpbsMacro)
        hl0.addItem(spacerItem)        


        hl = QtWidgets.QHBoxLayout()
        
        self.flwPins = PinTable(self)
        self.flwPins.load(_json)
        self.figure = SFigure()

        hl.addWidget(self.flwPins)
        hl.addWidget(self.figure)
        
        vl.addLayout(hl0)
        vl.addLayout(hl)
