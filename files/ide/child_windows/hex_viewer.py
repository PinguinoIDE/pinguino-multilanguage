#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
from math import ceil

from intelhex import IntelHex
from PySide import QtGui, QtCore

from ..methods.constants import NAME, TAB_NAME
from ...frames.hex_viewer_widget import Ui_HexViewer

########################################################################
class HexViewer(QtGui.QMainWindow):
    
    def __init__(self, parent, file_path):
        #QtGui.QMainWindow.__init__(self)
        super(HexViewer, self).__init__()
        #self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint |
                            #QtCore.Qt.WindowSystemMenuHint |
                            #QtCore.Qt.WindowStaysOnTopHint)        
        
        self.hex_viewer = Ui_HexViewer()
        self.hex_viewer.setupUi(self)
        self.main = parent
        
        self.setWindowTitle(TAB_NAME+" - "+self.windowTitle())
        
        self.original_filename = file_path
        
        self.hex_obj = IntelHex(file(file_path, "r"))
        self.update_viewer()
        
        self.connect(self.hex_viewer.comboBox_view, QtCore.SIGNAL("currentIndexChanged(QString)"), self.update_viewer)
        self.connect(self.hex_viewer.tableWidget_viewer, QtCore.SIGNAL("itemChanged(QTableWidgetItem*)"), lambda :self.hex_viewer.pushButton_save_changes.setEnabled(True))
        self.connect(self.hex_viewer.pushButton_close, QtCore.SIGNAL("clicked()"), self.close)
        self.connect(self.hex_viewer.pushButton_save_changes, QtCore.SIGNAL("clicked()"), self.save_changes)     
        
        self.centrar()

    #----------------------------------------------------------------------
    def centrar(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        
        
    #----------------------------------------------------------------------
    def save_changes(self):
        
        new_hex = IntelHex()
        new_hex.fromdict(self.get_table_dict())
        
        save_filename = QtGui.QFileDialog.getSaveFileName(self,
                NAME+" - Save",
                os.path.join(QtCore.QDir.home().path(), self.original_filename.replace(".hex", "_copy.hex")),
                "Hex files (*.hex;;All Files (*)")
        
        if save_filename:  
            new_hex.write_hex_file(save_filename[0])
        
    #----------------------------------------------------------------------
    def get_table_dict(self):
        
        dict_ = {}
        rows = self.hex_viewer.tableWidget_viewer.rowCount()
        
        space = 0
        for index in range(rows):
            
            for j in range(0x18):
                item = self.hex_viewer.tableWidget_viewer.item(index, j)
                if item:
                    value = self.get_dec_item(item.text())
                    if not value is None: dict_[space] = value
                    space += 1
        
        return dict_
        
        
    #----------------------------------------------------------------------
    def update_viewer(self, format_=None):
        
        hex_dict = self.hex_obj.todict()
        rows = int(ceil(max(hex_dict.keys()) / float(0x18)))
        self.hex_viewer.tableWidget_viewer.setRowCount(rows)
        
        space = 0
        for index in range(rows):
            
            item = QtGui.QTableWidgetItem()
            item.setText(hex(space)[hex(space).find("x")+1:].upper().rjust(6, "0"))
            self.hex_viewer.tableWidget_viewer.setVerticalHeaderItem(index, item) 
            
            for j in range(0x18):
                self.hex_viewer.tableWidget_viewer.setItem(index, j, QtGui.QTableWidgetItem())
                
                if index == rows - 1:
                    value = hex_dict.get(space, "FINISH")
                    if value == "FINISH":
                        self.update_width()
                        return
                else:
                    value = hex_dict.get(space, None)
                
                item = self.hex_viewer.tableWidget_viewer.item(index, j)
                item.setText(self.get_representation(value, format_))
                item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
                
                font = item.font()
                font.setFamily("mono")
                font.setPointSize(9)
                item.setFont(font)
                
                
                space += 1
                
        self.update_width()
        
    #----------------------------------------------------------------------
    def update_width(self):
        
        value = self.hex_viewer.tableWidget_viewer.item(0, 0).text()
        self.hex_viewer.tableWidget_viewer.horizontalHeader().setDefaultSectionSize(len(value)*12)
        self.hex_viewer.tableWidget_viewer.verticalHeader().setDefaultSectionSize(20)
        
                
    #----------------------------------------------------------------------
    def get_representation(self, value, format_):
        
        if value is None:
            value = 255
        
        if format_ is None:
            format_ = self.hex_viewer.comboBox_view.currentText()
        
        if format_ == "HEX (0xFF)":
            hex_ = hex(value)
            n_value = "0x"+hex_[hex_.find("x")+1:].upper().rjust(2, "0")
            
        elif format_ == "HEX (FF)":
            value = hex(value)
            n_value = value[value.find("x")+1:].upper().rjust(2, "0")
            
        elif format_ == "DEC":
            value = str(value)
            n_value = value[value.find("x")+1:].upper().rjust(2, "0")

        return n_value
    
    #----------------------------------------------------------------------
    def get_dec_item(self, value):
        
        value = value.replace(" ", "")
        if not value: return None
            
        format_ = self.hex_viewer.comboBox_view.currentText()
    
        if format_ == "HEX (0xFF)":
            n_value = eval(value)
            
        elif format_ == "HEX (FF)":
            n_value = n_value = eval("0x"+value)
            
        elif format_ == "DEC":
            n_value = int(value)
        
        return n_value
