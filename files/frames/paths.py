# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/yeison/Documentos/python/dev/developing/pinguino/pinguino-ide/qtgui/frames/paths.ui'
#
# Created: Sun Apr 27 15:31:29 2014
#      by: pyside-uic 0.2.14 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Paths(object):
    def setupUi(self, Paths):
        Paths.setObjectName("Paths")
        Paths.resize(737, 278)
        self.gridLayout_5 = QtGui.QGridLayout(Paths)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.groupBox = QtGui.QGroupBox(Paths)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_sdcc_bin = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_sdcc_bin.setObjectName("lineEdit_sdcc_bin")
        self.horizontalLayout.addWidget(self.lineEdit_sdcc_bin)
        self.pushButton_clear_sdcc_bin = QtGui.QPushButton(self.groupBox)
        self.pushButton_clear_sdcc_bin.setMaximumSize(QtCore.QSize(26, 16777215))
        self.pushButton_clear_sdcc_bin.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_clear_sdcc_bin.setIcon(icon)
        self.pushButton_clear_sdcc_bin.setFlat(True)
        self.pushButton_clear_sdcc_bin.setObjectName("pushButton_clear_sdcc_bin")
        self.horizontalLayout.addWidget(self.pushButton_clear_sdcc_bin)
        self.pushButton_sdcc_bin = QtGui.QPushButton(self.groupBox)
        self.pushButton_sdcc_bin.setObjectName("pushButton_sdcc_bin")
        self.horizontalLayout.addWidget(self.pushButton_sdcc_bin)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEdit_pinguino_8_libs = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_pinguino_8_libs.setObjectName("lineEdit_pinguino_8_libs")
        self.horizontalLayout_3.addWidget(self.lineEdit_pinguino_8_libs)
        self.pushButton_clear_8_libs = QtGui.QPushButton(self.groupBox)
        self.pushButton_clear_8_libs.setMaximumSize(QtCore.QSize(26, 16777215))
        self.pushButton_clear_8_libs.setText("")
        self.pushButton_clear_8_libs.setIcon(icon)
        self.pushButton_clear_8_libs.setFlat(True)
        self.pushButton_clear_8_libs.setObjectName("pushButton_clear_8_libs")
        self.horizontalLayout_3.addWidget(self.pushButton_clear_8_libs)
        self.pushButton_pinguino_8_libs = QtGui.QPushButton(self.groupBox)
        self.pushButton_pinguino_8_libs.setObjectName("pushButton_pinguino_8_libs")
        self.horizontalLayout_3.addWidget(self.pushButton_pinguino_8_libs)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(Paths)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lineEdit_gcc_bin = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_gcc_bin.setObjectName("lineEdit_gcc_bin")
        self.horizontalLayout_4.addWidget(self.lineEdit_gcc_bin)
        self.pushButton_clear_gcc_bin = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_clear_gcc_bin.setMaximumSize(QtCore.QSize(26, 16777215))
        self.pushButton_clear_gcc_bin.setText("")
        self.pushButton_clear_gcc_bin.setIcon(icon)
        self.pushButton_clear_gcc_bin.setFlat(True)
        self.pushButton_clear_gcc_bin.setObjectName("pushButton_clear_gcc_bin")
        self.horizontalLayout_4.addWidget(self.pushButton_clear_gcc_bin)
        self.pushButton_gcc_bin = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_gcc_bin.setObjectName("pushButton_gcc_bin")
        self.horizontalLayout_4.addWidget(self.pushButton_gcc_bin)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 0, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lineEdit_pinguino_32_libs = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_pinguino_32_libs.setObjectName("lineEdit_pinguino_32_libs")
        self.horizontalLayout_5.addWidget(self.lineEdit_pinguino_32_libs)
        self.pushButton_clear_32_libs = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_clear_32_libs.setMaximumSize(QtCore.QSize(26, 16777215))
        self.pushButton_clear_32_libs.setText("")
        self.pushButton_clear_32_libs.setIcon(icon)
        self.pushButton_clear_32_libs.setFlat(True)
        self.pushButton_clear_32_libs.setObjectName("pushButton_clear_32_libs")
        self.horizontalLayout_5.addWidget(self.pushButton_clear_32_libs)
        self.pushButton_pinguino_32_libs = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_pinguino_32_libs.setObjectName("pushButton_pinguino_32_libs")
        self.horizontalLayout_5.addWidget(self.pushButton_pinguino_32_libs)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 1, 1, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtGui.QSpacerItem(304, 23, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_close = QtGui.QPushButton(Paths)
        self.pushButton_close.setMinimumSize(QtCore.QSize(165, 0))
        self.pushButton_close.setObjectName("pushButton_close")
        self.horizontalLayout_2.addWidget(self.pushButton_close)
        self.gridLayout_5.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.retranslateUi(Paths)
        QtCore.QMetaObject.connectSlotsByName(Paths)

    def retranslateUi(self, Paths):
        Paths.setWindowTitle(QtGui.QApplication.translate("Paths", "Paths", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Paths", "8-bit", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Paths", "SDCC compiler:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_sdcc_bin.setText(QtGui.QApplication.translate("Paths", "Change...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Paths", "Libraries:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_pinguino_8_libs.setText(QtGui.QApplication.translate("Paths", "Change...", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Paths", "32-bit", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Paths", "GCC compiler:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_gcc_bin.setText(QtGui.QApplication.translate("Paths", "Change...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Paths", "Libraries:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_pinguino_32_libs.setText(QtGui.QApplication.translate("Paths", "Change...", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_close.setText(QtGui.QApplication.translate("Paths", "Close", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
