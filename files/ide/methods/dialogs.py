#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

from PySide import QtGui, QtCore

from .constants import NAME

########################################################################
class Dialogs(object):
    
    #----------------------------------------------------------------------
    @classmethod
    def set_save_file(self, parent, filename):
        if filename.endswith("*"): filename = filename[:-1]
        ext = os.path.splitext(os.path.split(filename)[1])[1]
        save_filename = QtGui.QFileDialog.getSaveFileName(parent,
                NAME+QtGui.QApplication.translate("Dialogs", " - Save"), 
                os.path.join(QtCore.QDir.home().path(), filename),
                QtGui.QApplication.translate("Dialogs", "Pinguino files (*%s);;All Files (*)")%ext) 
        if save_filename: return save_filename[0], os.path.split(save_filename[0])[1]
        else: return None
        
    #----------------------------------------------------------------------
    @classmethod
    def set_open_file(self, parent):
        open_files = QtGui.QFileDialog.getOpenFileNames(parent,
                NAME+QtGui.QApplication.translate("Dialogs", " - Open"),
                QtCore.QDir.home().path(),
                QtGui.QApplication.translate("Dialogs", "Pinguino Files (*.pde *.gpde);;All Files (*)"))
        if open_files: return open_files[0]
        else: return None
            

    #----------------------------------------------------------------------
    @classmethod
    def set_no_saved_file(self, parent, filename):
        
        options = QtGui.QMessageBox.Yes | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel
        reply = QtGui.QMessageBox.question(parent,
                NAME+QtGui.QApplication.translate("Dialogs", " - Save"),
                QtGui.QApplication.translate("Dialogs", "This file has not been saved,\nWould you like to do?\n\n")+filename,
                options)
        
        if reply == QtGui.QMessageBox.Yes: return True
        elif reply == QtGui.QMessageBox.Discard: return False
        else: return None
        
        
    #----------------------------------------------------------------------
    @classmethod
    def set_open_dir(self, parent):
        
        open_dir = QtGui.QFileDialog.getExistingDirectory(parent,
                NAME+QtGui.QApplication.translate("Dialogs", " - Open directory"),
                QtCore.QDir.home().path())
        
        if open_dir: return open_dir
        else: return None
        
    #----------------------------------------------------------------------
    @classmethod
    def file_duplicated(self, parent, filename):
        
        QtGui.QMessageBox.information(parent,
                NAME+QtGui.QApplication.translate("Dialogs", " - File already open"),
                QtGui.QApplication.translate("Dialogs", "This file is already open in other tab.\n%s")%filename)
        return True
    
    #----------------------------------------------------------------------
    @classmethod
    def error_message(self, parent, message):
        
        QtGui.QMessageBox.warning(parent,
                NAME+QtGui.QApplication.translate("Dialogs", " - Error"),
                message)
        return True
        
    #----------------------------------------------------------------------
    @classmethod
    def confirm_message(self, parent, message):
        
        options = QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel
        reply = QtGui.QMessageBox.question(parent,
                NAME+QtGui.QApplication.translate("Dialogs", " - Confirmation"),
                message,
                options)
        
        if reply == QtGui.QMessageBox.Yes: return True
        elif reply == QtGui.QMessageBox.Discard: return False
        else: return None
                
        
    #----------------------------------------------------------------------
    @classmethod
    def info_message(self, parent, message):
        
        QtGui.QMessageBox.information(parent,
                NAME+QtGui.QApplication.translate("Dialogs", " - Information"),
                message)
        return True
    
    #----------------------------------------------------------------------
    @classmethod
    def warning_message(self, parent, message):
        
        QtGui.QMessageBox.warning(parent,
                NAME+QtGui.QApplication.translate( "Dialogs", " - Warning"),
                message)
        return True
            
    #----------------------------------------------------------------------
    @classmethod
    def save_before_compile(self, parent):
        
        QtGui.QMessageBox.information(parent,
                NAME+QtGui.QApplication.translate("Dialogs", " - Save file first."),
                QtGui.QApplication.translate("Dialogs", "You must save the file before compiling."))
        return True
    
    #----------------------------------------------------------------------
    @classmethod
    def confirm_board(self, parent):
        
        parent.set_board()
        board_config = parent.get_description_board()
        
        msg_box = QtGui.QMessageBox()
        msg_box.setIcon(QtGui.QMessageBox.Question)
        msg_box.setWindowTitle(NAME+QtGui.QApplication.translate("Dialogs", " - Config board"))
        msg_box.setText(board_config+QtGui.QApplication.translate("Dialogs", "\n\nUse this board config?"))
        
        cancel = QtGui.QPushButton()
        cancel.setText(QtGui.QApplication.translate("Dialogs", "Cancel"))
        
        change = QtGui.QPushButton()
        change.setText(QtGui.QApplication.translate("Dialogs", "Change board"))
        
        compile_ = QtGui.QPushButton()
        compile_.setText(QtGui.QApplication.translate("Dialogs", "Compile"))
        
        msg_box.addButton(cancel, QtGui.QMessageBox.RejectRole)
        msg_box.addButton(change, QtGui.QMessageBox.NoRole)
        msg_box.addButton(compile_, QtGui.QMessageBox.YesRole)
        
        msg_box.setDefaultButton(compile_)
        
        reply = msg_box.exec_()    
        
        if reply == 2: return True
        elif reply == 1: return False
        else: return None
        
        
    #----------------------------------------------------------------------
    @classmethod
    def error_while_compiling(self, parent):
        
        msg_box = QtGui.QMessageBox()
        msg_box.setIcon(QtGui.QMessageBox.Warning)
        msg_box.setWindowTitle(NAME+QtGui.QApplication.translate("Dialogs", " - Error"))
        msg_box.setText(QtGui.QApplication.translate("Dialogs", "Error while compiling."))
        
        stdout = QtGui.QPushButton()
        stdout.setText(QtGui.QApplication.translate("Dialogs", "View stdout"))
        
        ok = QtGui.QPushButton()
        ok.setText(QtGui.QApplication.translate("Dialogs", "Ok"))
        
        msg_box.addButton(stdout, QtGui.QMessageBox.RejectRole)
        msg_box.addButton(ok, QtGui.QMessageBox.NoRole)
        
        msg_box.setDefaultButton(ok)
        
        reply = msg_box.exec_()    
        
        if reply == 0: return True
        elif reply == 1: return False
    
    #----------------------------------------------------------------------
    @classmethod
    def error_while_linking(self, parent):
        
        msg_box = QtGui.QMessageBox()
        msg_box.setIcon(QtGui.QMessageBox.Warning)
        msg_box.setWindowTitle(NAME+QtGui.QApplication.translate("Dialogs", " - Error"))
        msg_box.setText(QtGui.QApplication.translate("Dialogs", "Error while linking."))
        
        stdout = QtGui.QPushButton()
        stdout.setText(QtGui.QApplication.translate("Dialogs", "View stdout"))
        
        ok = QtGui.QPushButton()
        ok.setText(QtGui.QApplication.translate("Dialogs", "Ok"))
        
        msg_box.addButton(stdout, QtGui.QMessageBox.RejectRole)
        msg_box.addButton(ok, QtGui.QMessageBox.NoRole)
        
        msg_box.setDefaultButton(ok)
        
        reply = msg_box.exec_()    
        
        if reply == 0: return True
        elif reply == 1: return False
        
    
    #----------------------------------------------------------------------
    @classmethod
    def error_while_preprocess(self, parent):
        
        msg_box = QtGui.QMessageBox()
        msg_box.setIcon(QtGui.QMessageBox.Warning)
        msg_box.setWindowTitle(NAME+QtGui.QApplication.translate("Dialogs", " - Error"))
        msg_box.setText(QtGui.QApplication.translate("Dialogs", "Error while preprocess."))
        
        stdout = QtGui.QPushButton()
        stdout.setText(QtGui.QApplication.translate("Dialogs", "View stdout"))
        
        ok = QtGui.QPushButton()
        ok.setText(QtGui.QApplication.translate("Dialogs", "Ok"))
        
        msg_box.addButton(stdout, QtGui.QMessageBox.RejectRole)
        msg_box.addButton(ok, QtGui.QMessageBox.NoRole)
        
        msg_box.setDefaultButton(ok)
        
        reply = msg_box.exec_()    
        
        if reply == 0: return True
        elif reply == 1: return False
        
        
    
    #----------------------------------------------------------------------
    @classmethod
    def error_while_unknow(self, parent):
        
        msg_box = QtGui.QMessageBox()
        msg_box.setIcon(QtGui.QMessageBox.Warning)
        msg_box.setWindowTitle(NAME+QtGui.QApplication.translate("Dialogs", " - Error"))
        msg_box.setText(QtGui.QApplication.translate("Dialogs", "Unknow error."))
        
        stdout = QtGui.QPushButton()
        stdout.setText(QtGui.QApplication.translate("Dialogs", "View stdout"))
        
        ok = QtGui.QPushButton()
        ok.setText(QtGui.QApplication.translate("Dialogs", "Ok"))
        
        msg_box.addButton(stdout, QtGui.QMessageBox.RejectRole)
        msg_box.addButton(ok, QtGui.QMessageBox.NoRole)
        
        msg_box.setDefaultButton(ok)
        
        reply = msg_box.exec_()    
        
        if reply == 0: return True
        elif reply == 1: return False
                
                
        
    #----------------------------------------------------------------------
    @classmethod
    def compilation_done(self, parent):
        
        msg_box = QtGui.QMessageBox()
        msg_box.setIcon(QtGui.QMessageBox.Information)
        msg_box.setWindowTitle(NAME+QtGui.QApplication.translate("Dialogs", " - Compiled"))
        msg_box.setText(QtGui.QApplication.translate("Dialogs", "Compilation done!"))
        
        upload = QtGui.QPushButton()
        upload.setText(QtGui.QApplication.translate("Dialogs", "Upload now!"))
        
        ok = QtGui.QPushButton()
        ok.setText(QtGui.QApplication.translate("Dialogs", "Ok"))
        
        msg_box.addButton(upload, QtGui.QMessageBox.AcceptRole)
        msg_box.addButton(ok, QtGui.QMessageBox.NoRole)
        
        msg_box.setDefaultButton(ok)
        
        reply = msg_box.exec_()    
        
        if reply == 0: return True
        elif reply == 1: return False
        
    #----------------------------------------------------------------------
    @classmethod
    def upload_done(self, parent):
        
        QtGui.QMessageBox.information(parent,
                NAME+QtGui.QApplication.translate("Dialogs", " - Upload done"),
                QtGui.QApplication.translate("Dialogs", "File sucessfully uploaded to pinguino."))
        return True
    
        
    #----------------------------------------------------------------------
    @classmethod
    def upload_fail(self, parent, message):
        
        msg_box = QtGui.QMessageBox()
        msg_box.setIcon(QtGui.QMessageBox.Information)
        msg_box.setWindowTitle(NAME+QtGui.QApplication.translate("Dialogs", " - Upload fail"))
        msg_box.setText(message)
        
        upload = QtGui.QPushButton()
        upload.setText(QtGui.QApplication.translate("Dialogs", "Try again!!"))
        
        ok = QtGui.QPushButton()
        ok.setText(QtGui.QApplication.translate("Dialogs", "Cancel"))
        
        msg_box.addButton(upload, QtGui.QMessageBox.AcceptRole)
        msg_box.addButton(ok, QtGui.QMessageBox.NoRole)
        
        msg_box.setDefaultButton(upload)
        
        reply = msg_box.exec_()    
        
        if reply == 0: return True
        elif reply == 1: return False
        
        
    #----------------------------------------------------------------------
    @classmethod
    def set_save_image(self, parent, filename):
        
        file_name = QtGui.QFileDialog.getSaveFileName(parent,
                NAME+QtGui.QApplication.translate("Dialogs", " - Save image"),
                filename,
                QtGui.QApplication.translate("Dialogs", "Png files (*.png);;All Files (*)"))
        
        if file_name: return file_name[0]
        else: return None