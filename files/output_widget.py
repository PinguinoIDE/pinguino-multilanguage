#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys

from PySide import QtCore, QtGui
import git

from ..methods import constants as Constants
from ..methods.python_shell import PythonShell

HEAD = Constants.TAB_NAME + "\n" + "Python " + sys.version + " on " + sys.platform
HELP = QtGui.QApplication.translate("PythonShell", "can also use the commands:") + '"clear", "restart"'

START = ">>> "


########################################################################
class PinguinoTerminal(QtGui.QPlainTextEdit):
    
    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(PinguinoTerminal, self).__init__(*args, **kwargs)
        
        self.setStyleSheet("background-color: #333;"\
                           "color: #fff;"\
                           "font-family: mono;"\
                           "font-size: 12px;")
        
        self.appendPlainText(HEAD)
        self.appendPlainText(HELP)
        self.appendPlainText(START)
        
        self.extra_args = {}
        
        self.shell = PythonShell()
        
        self.historial = []
        self.index_historial = 0
        

    #----------------------------------------------------------------------
    def keyPressEvent(self, event):
        
        self.set_last_line()
        
        if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Enter-1):
            self.moveCursor(QtGui.QTextCursor.End)
            self.index_historial = 0
            super(PinguinoTerminal, self).keyPressEvent(event)
            command = self.get_command()
            if self.run_default_command(command):
                self.appendPlainText(START)
                return
            self.historial.append(command.replace("\n", ""))
            if not command.isspace():
                self.moveCursor(QtGui.QTextCursor.End)
                self.insertPlainText(self.shell.run(command))
            self.insertPlainText(START)
            self.moveCursor(QtGui.QTextCursor.End)
    
        elif event.key() == QtCore.Qt.Key_Backspace:
            if not self.get_command(): return
            else: super(PinguinoTerminal, self).keyPressEvent(event)
            
        elif event.key() == QtCore.Qt.Key_Up:
            if len(self.historial) >= self.index_historial + 1:
                self.index_historial += 1
                self.moveCursor(QtGui.QTextCursor.End)
                
                tc = self.textCursor()
                tc.movePosition(tc.StartOfLine, tc.KeepAnchor)
                tc.removeSelectedText()
                tc.insertText(START)
                
                tc.insertText(self.historial[-self.index_historial])
                
        elif event.key() == QtCore.Qt.Key_Down:
            if len(self.historial) >= self.index_historial - 1:
                self.index_historial -= 1
                if self.index_historial <= 0:
                    self.index_historial += 1
                    return
                self.moveCursor(QtGui.QTextCursor.End)
                
                tc = self.textCursor()
                tc.movePosition(tc.StartOfLine, tc.KeepAnchor)
                tc.removeSelectedText()
                tc.insertText(START)
                
                tc.insertText(self.historial[-self.index_historial])
            
        elif event.key() == QtCore.Qt.Key_Left:
            if self.no_overwrite_start():
                super(PinguinoTerminal, self).keyPressEvent(event)
        
        else:
            super(PinguinoTerminal, self).keyPressEvent(event)
            
            
    #----------------------------------------------------------------------
    def get_command(self):
        
        plain = self.toPlainText()
        comand = plain[plain.rfind(START):]
        return comand[len(START):]
    

    #----------------------------------------------------------------------
    def wheelEvent(self, event):
        
        if event.modifiers() == QtCore.Qt.ControlModifier:
            self.step_font_size(event.delta())
            
        else: super(PinguinoTerminal, self).wheelEvent(event)
                
                
    #----------------------------------------------------------------------
    def contextMenuEvent(self, event):
        pass
                
    #----------------------------------------------------------------------
    def step_font_size(self, delta):
        
        font = self.font()
        size = font.pointSize()
        if delta > 0: font.setPointSize(size+1)
        else: font.setPointSize(size-1)
        self.setFont(font)
                          
                          
    #----------------------------------------------------------------------
    def set_extra_args(self, *args, **kwargs):
        
        for key in kwargs:
            setattr(self.shell.statement_module, key, kwargs[key])
            
            
        self.extra_args.update(kwargs)
        
                          
    #----------------------------------------------------------------------
    def set_last_line(self):
        
        cursor = self.textCursor()
        position = cursor.position()
        plain = self.toPlainText()
        index = plain.rfind("\n")
        if position < (index + len(START) + 1): self.moveCursor(QtGui.QTextCursor.End)
        
                          
    #----------------------------------------------------------------------
    def no_overwrite_start(self):
        
        cursor = self.textCursor()
        position = cursor.position()
        plain = self.toPlainText()
        index = plain.rfind("\n")
        if position > index:
            return (position - index) > len(START) + 1
        #if position < index: self.moveCursor(QtGui.QTextCursor.End)
        
        
    #----------------------------------------------------------------------
    def run_default_command(self, command):
        
        command = command.replace("\n", "")
        run = getattr(self, "command_"+command, None)
        if run: run()
        
        return bool(run)
        
        
    #----------------------------------------------------------------------
    def command_clear(self):
        
        self.clear()
        
        
    #----------------------------------------------------------------------
    def command_restart(self):
        
        self.shell.restart()
        self.clear()
        self.appendPlainText(HEAD)
        self.appendPlainText(HELP)
        self.set_extra_args(**self.extra_args)
        #self.main.plainTextEdit_output.shell.statement_module.pinguino_main = self       