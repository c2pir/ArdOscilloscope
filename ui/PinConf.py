# -*- coding: utf-8 -*-
"""
UI classes for pins list
"""

from PyQt5 import QtCore, QtGui, QtWidgets

class PinTable(QtWidgets.QTableWidget):
    """Table of pins configurations"""
    sChangeMode = QtCore.pyqtSignal(dict)   # signal send when a mode combobox selection change
    sChangeWatch = QtCore.pyqtSignal(dict)  # signal send when a watch checkbox change state
    
    def __init__(self, parent=None):
        QtWidgets.QTableWidget.__init__(self, parent)
        
        #Column count
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["watch", "pin", "mode", "value"])

        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.verticalHeader().setVisible(False)

        self.setMaximumWidth(300)
        self.itemChanged.connect(self.update_pin_name)

    def load(self, json):
        """Load and show a json config file."""
        self.blockSignals(True)
        self.json = json
        self.setRowCount(len(json))
        i = 0
        for conf in json:
            cb = CBWatch()
            cb.cb.stateChanged.connect(lambda x, index=i: self.update_watch(x, index))
            if conf["watch"]==2:
                cb.cb.setChecked(True)
            self.setCellWidget(i,0,cb)
            
            item = QtWidgets.QTableWidgetItem(conf["name"])
            item.index = i
            self.setItem(i,1, item)
            
            
            cbb = CBBMode(conf["type"])
            cbb.currentIndexChanged.connect(lambda x, index=i: self.update_mode(x, index))
            cbb.setCurrentIndex(conf["mode"])
            self.setCellWidget(i, 2, cbb)
            
            itemv = QtWidgets.QTableWidgetItem("")
            itemv.setFlags(QtCore.Qt.ItemIsEnabled)
            self.setItem(i,3, itemv)
            
            i+=1
        
        self.blockSignals(False)
        self.resizeColumnsToContents()

    def update_watch(self, x, i):
        """Callback for watch column edition"""
        try:
            self.json[i]["watch"] = x
            self.sChangeWatch.emit(self.json[i])
        except Exception as e:
            print(e)

    def update_mode(self, x, i):
        """Callback for mode column edition"""
        try:
            self.json[i]["mode"] = x
            self.sChangeMode.emit(self.json[i])
        except Exception as e:
            print(e)
    
    def update_pin_name(self, x):
        """Callback for name column edition"""
        try:
            self.json[x.index]["name"] = x.text()
            self.resizeColumnsToContents()
        except Exception as e:
            print(e)

class CBWatch(QtWidgets.QWidget):
    """ CheckBox Field """
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.cb = QtWidgets.QCheckBox()
        hl = QtWidgets.QHBoxLayout(self)
        hl.addWidget(self.cb)
        hl.setAlignment(QtCore.Qt.AlignCenter)
        hl.setContentsMargins(0,0,0,0)

class CBBMode(QtWidgets.QComboBox):
    """ Combobox Field """
    def __init__(self, type_, parent=None):
        QtWidgets.QComboBox.__init__(self, parent)
        options = ["Unused"]
        if "I" in type_:
            options.append("Read")
        if "O" in type_:
            options.append("Write")
        if "PWM" in type_:
            options.append("PWM")
        self.addItems(options)


