#!/usr/bin/env python
#-*- coding: utf-8 -*-

import codecs
import os

from PySide import QtGui, QtCore

#from ..methods.constants import os.getenv("NAME")
#from ..methods.constants import PINGUINO_STDOUT_FILE
from ...frames.stdout import Ui_PlainOut
from ..code_editor.pinguino_highlighter import Highlighter

########################################################################
class PlainOut(QtGui.QDialog):

    def __init__(self, title):
        super(PlainOut, self).__init__()


        self.plain_out = Ui_PlainOut()
        self.plain_out.setupUi(self)

        self.plain_out.textEdit.setStyleSheet("""
        QTextEdit {
            background-color: #FFF;
            font-family: ubuntu mono;
            font-weight: normal;
            font-size: 11pt;
            }

        """)

        self.setWindowTitle(os.getenv("NAME")+" - "+title)

        self.connect(self.plain_out.pushButton_close, QtCore.SIGNAL("clicked()"), self.close)

        palette = QtGui.QPalette(self.palette())
        self.setAutoFillBackground(True)
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor("#FFFFFF"))
        self.setPalette(palette)

        PINGUINO_STDOUT_FILE = os.path.join(os.getenv("PINGUINO_USER_PATH"), "source", "stdout")

        if os.path.exists(PINGUINO_STDOUT_FILE):
            stdout = codecs.open(PINGUINO_STDOUT_FILE, "r", "utf-8")
            content = stdout.readlines()
            stdout.close()
            self.show_text("".join(content))

        self.plain_out.pushButton_close.setFocus()

        self.setStyleSheet("""
        font-family: ubuntu regular;
        font-weight: normal;

        """)

        self.center_on_screen()


    #----------------------------------------------------------------------

    def center_on_screen(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)


    #----------------------------------------------------------------------
    def show_text(self, text, pde=False):

        if pde: Highlighter(self.plain_out.textEdit)
        self.plain_out.textEdit.setPlainText(text)
