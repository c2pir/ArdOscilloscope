# -*- coding: utf-8 -*-
"""
"""

from PyQt5 import QtCore, QtGui, QtWidgets

class CBField(QtWidgets.QWidget):
    """ Combobox Field """
    def __init__(self, name, options=[], parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        horizontalLayout = QtWidgets.QHBoxLayout(self)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        
        self.l = QtWidgets.QLabel(self)
        self.l.setText(str(name)+":")
        self.cb = QtWidgets.QComboBox(self)
        #self.cb.setEditable(True)
        #spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        
        horizontalLayout.addWidget(self.l)
        horizontalLayout.addWidget(self.cb)
        #horizontalLayout.addItem(spacerItem)

        self.load(options)

    def load(self, options):
        """ """
        self.cb.clear()
        self.cb.addItems([str(o) for o in options])
        self.resize(self.sizeHint())
        

class PBField(QtWidgets.QPushButton):
    def __init__(self, path="", tool_tip="", parent=None):
        QtWidgets.QPushButton.__init__(self, parent)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.setIcon(icon)
        self.setToolTip(tool_tip)


class SBField(QtWidgets.QWidget):
    """ SpinBox Field """
    def __init__(self, name, options=[], parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        horizontalLayout = QtWidgets.QHBoxLayout(self)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        
        self.l = QtWidgets.QLabel(self)
        self.l.setText(str(name)+":")
        self.sb = QtWidgets.QSpinBox()

        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        
        horizontalLayout.addWidget(self.l)
        horizontalLayout.addWidget(self.sb)
        horizontalLayout.addItem(spacerItem)


