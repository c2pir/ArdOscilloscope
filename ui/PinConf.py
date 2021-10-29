# -*- coding: utf-8 -*-
"""
"""

from PyQt5 import QtCore, QtGui, QtWidgets

class PinTable(QtWidgets.QTableWidget):
    """ """
    sChangeMode = QtCore.pyqtSignal(dict)
    sChangeWatch = QtCore.pyqtSignal(dict)
    
    def __init__(self, parent=None):
        QtWidgets.QTableWidget.__init__(self, parent)
        
        #Column count
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["watch","pin", "mode"])

        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.verticalHeader().setVisible(False)

        self.setMaximumWidth(300)

    def load(self, json):
        self.json = json
        self.setRowCount(len(json))
        i = 0
        for conf in json:
            cb = CBWatch()
            
            cb.cb.stateChanged.connect(lambda x, index=i: self.update_watch(x, index))
            if conf["watch"]==2:
                cb.cb.setChecked(True)
            self.setCellWidget(i,0,cb)

            self.setItem(i,1, QtWidgets.QTableWidgetItem(conf["name"]))
            
            cbb = CBBMode(conf["type"])
            cbb.currentIndexChanged.connect(lambda x, index=i: self.update_mode(x, index))
            cbb.setCurrentIndex(conf["mode"])
            self.setCellWidget(i, 2, cbb)
            i+=1
        self.resizeColumnsToContents()

    def update_watch(self, x, i):
        try:
            self.json[i]["watch"] = x
            self.sChangeWatch.emit(self.json[i])
        except Exception as e:
            print(e)

    def update_mode(self, x, i):
        try:
            self.json[i]["mode"] = x
            self.sChangeMode.emit(self.json[i])
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
        self.addItems(options)


