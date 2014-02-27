#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PySide import QtGui, QtCore

from ..methods.constants import TAB_NAME
from ...frames.about import Ui_About

########################################################################
class About(QtGui.QDialog):
    
    def __init__(self, IDE):
        super(About, self).__init__()     
    
        self.about = Ui_About()
        self.about.setupUi(self)
        
        self.setWindowTitle(TAB_NAME+" - "+self.windowTitle())
        
        
        self.connect(self.about.pushButton_credits, QtCore.SIGNAL("clicked()"), lambda :self.about.stackedWidget.setCurrentIndex(1))
        self.connect(self.about.pushButton_license, QtCore.SIGNAL("clicked()"), lambda :self.about.stackedWidget.setCurrentIndex(2))
        self.connect(self.about.pushButton_about, QtCore.SIGNAL("clicked()"), lambda :self.about.stackedWidget.setCurrentIndex(0))
        self.connect(self.about.pushButton_close, QtCore.SIGNAL("clicked()"), self.close)
        self.connect(self.about.pushButton_close_2, QtCore.SIGNAL("clicked()"), self.close)
        self.connect(self.about.pushButton_close_3, QtCore.SIGNAL("clicked()"), self.close)
        
        self.about.stackedWidget.setCurrentIndex(0)
        self.about.tabWidget.setCurrentIndex(0)
