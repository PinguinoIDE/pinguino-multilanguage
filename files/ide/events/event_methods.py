#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import codecs
import webbrowser

from PySide import QtCore, QtGui

from ..code_editor.pinguino_code_editor import PinguinoCodeEditor
from ..methods.syntax import Snippet
from ..methods.dialogs import Dialogs
from ..methods.decorators import Decorator
from ..methods import constants as Constants
from ..methods.methods import Methods
from ..child_windows.about import About
from ..child_windows.board_config import BoardConfig
from ..child_windows.plain_text_out import PlainOut
from ..child_windows.libraries import LibManager
from ..child_windows.paths import Paths
from ..child_windows.hex_viewer import HexViewer
from ..widgets.wiki_widget import WikiDock


########################################################################
class EventMethods(Methods):
    
    # Menu File
    
    #----------------------------------------------------------------------
    @Decorator.connect_features()
    def new_file(self, *args, **kwargs):
        path = kwargs.get("filename", self.__get_name__())
        filename = os.path.split(path)[1]         
        editor = PinguinoCodeEditor()
        self.main.tabWidget_files.addTab(editor, filename)
        editor.text_edit.insertPlainText(Snippet["file {snippet}"][1].replace("\t", ""))
        editor.text_edit.insertPlainText("\n")
        editor.text_edit.insertPlainText(Snippet["Bare minimum {snippet}"][1].replace("\t", ""))
        self.main.tabWidget_files.setCurrentWidget(editor)
        editor.text_edit.textChanged.connect(self.__text_changed__)
        editor.text_edit.undoAvailable.connect(self.__text_can_undo__)
        editor.text_edit.redoAvailable.connect(self.__text_can_redo__)
        editor.text_edit.copyAvailable.connect(self.__text_can_copy__)
        editor.text_edit.dropEvent = self.__drop__
        editor.text_edit.keyPressEvent = self.__key_press__
        self.main.tabWidget_files.setTabText(self.main.tabWidget_files.currentIndex(), filename[:-1])
            
    
    #----------------------------------------------------------------------
    def open_files(self):
        filenames = Dialogs.set_open_file(self)
        for filename in filenames:
            if self.__check_duplicate_file__(filename): continue

            self.update_recents(filename)
            if filename.endswith(".gpde"):
                self.switch_ide_mode(True)
                self.PinguinoKIT.open_files(filename=filename)
                return
            elif filename.endswith(".pde"):
                self.switch_ide_mode(False)                
                
            self.new_file(os.path.split(filename)[1])
            editor = self.main.tabWidget_files.currentWidget()
            pde_file = codecs.open(filename, "r", "utf-8")
            content = "".join(pde_file.readlines())
            pde_file.close()
            editor.text_edit.setPlainText(content)
            setattr(editor, "path", filename)
            self.main.tabWidget_files.setTabToolTip(self.main.tabWidget_files.currentIndex(), filename)
            self.main.tabWidget_files.setTabText(self.main.tabWidget_files.currentIndex(), os.path.split(filename)[1]) 
            #self.update_recents(filename)
            
        self.tab_changed()
    
    
    #----------------------------------------------------------------------
    @Decorator.connect_features()
    def save_file(self, *args, **kwargs):
        editor = kwargs.get("editor", None)
        if not editor: editor = self.get_tab().currentWidget()
        index = self.get_tab().indexOf(editor)
        filename = self.main.tabWidget_files.tabText(index)
        save_path = getattr(editor, "path", None)
        
        if not save_path:
            save_path, filename = Dialogs.set_save_file(self, filename)
            if not save_path: return False
            setattr(editor, "path", save_path)
            self.main.tabWidget_files.setTabText(index, filename)
            self.main.tabWidget_files.setTabToolTip(index, save_path)    
            self.setWindowTitle(Constants.TAB_NAME+" - "+save_path)
            
            self.update_recents(save_path)            
        
        self.__save_file__(editor=editor)
        return True
    
    
    #----------------------------------------------------------------------
    @Decorator.requiere_open_files()
    def close_file(self, *args, **kwargs):
        editor = kwargs.get("editor", None)
        if not editor: editor = self.get_tab().currentWidget()
        index = self.get_tab().indexOf(editor)
        filename = self.get_tab().tabText(index)
        save_path = getattr(editor, "path", None)
        
        if not save_path and filename.endswith("*"):
            reply = Dialogs.set_no_saved_file(self, filename)
            
            if reply == True:
                save_path, filename = Dialogs.set_save_file(self, filename)
                if not save_path: return
                setattr(editor, "path", save_path)
                self.__save_file__(editor)
                
            elif reply == None: return
            
        elif filename.endswith("*"):
            reply = Dialogs.set_no_saved_file(self, filename)
            #print reply
            if reply == True: self.__save_file__(editor)
            elif reply == None: return            
            
        self.get_tab().removeTab(index)
        
        
    #----------------------------------------------------------------------
    @Decorator.requiere_open_files()
    @Decorator.connect_features()
    def save_as(self, *args, **kwargs):
        editor = kwargs.get("editor", None)
        if not editor: editor = self.get_tab().currentWidget()
        index = self.get_tab().indexOf(editor)
        #editor = self.main.tabWidget_files.currentWidget()
        #index = self.main.tabWidget_files.currentIndex()
        filename = self.main.tabWidget_files.tabText(index)
        save_path = getattr(editor, "path", None)
        
        save_path, filename = Dialogs.set_save_file(self, filename)
        if not save_path: return False
        setattr(editor, "path", save_path)
        self.main.tabWidget_files.setTabText(index, filename)
        self.main.tabWidget_files.setTabToolTip(index, save_path) 
        self.setWindowTitle(Constants.TAB_NAME+" - "+save_path)
        
        self.__save_file__(editor=editor)
        return True
    
    
    #----------------------------------------------------------------------
    @Decorator.requiere_open_files()
    def save_all(self):
        tab = self.get_tab()
        for index in range(tab.count()):
            self.save_file(editor=tab.widget(index))
        
    
    #----------------------------------------------------------------------
    @Decorator.requiere_open_files()
    def close_all(self):
        tab = self.get_tab()
        widgets = map(lambda index:tab.widget(index), range(tab.count()))
        for widget in widgets:
            self.close_file(editor=widget)
                    
        
    #----------------------------------------------------------------------
    def __close_ide__(self, *args, **kwargs):
        size = self.size()
        self.configIDE.set("Main", "size", size.toTuple())
        
        pos = self.pos()
        self.configIDE.set("Main", "position", pos.toTuple())
        
        self.configIDE.set("Main", "maximized", self.isMaximized())
        
        count = 1
        for file_ in self.recent_files:
            self.configIDE.set("Recents", "recent_"+str(count), file_)
            count += 1
            
        count = 1
        self.configIDE.clear_recents_open()
        for file_ in self.get_all_open_files():
            self.configIDE.set("Recents", "open_"+str(count), file_)
            count += 1
            
        self.configIDE.set("Features", "graphical", self.is_graphical())
            
        self.configIDE.save_config()
        
        self.close()
    
    
    # Menu Edit
    
    #----------------------------------------------------------------------
    def undo(self):
        editor = self.main.tabWidget_files.currentWidget()
        index = self.main.tabWidget_files.currentIndex()
        editor.text_edit.undo()
        
        
    #----------------------------------------------------------------------
    def redo(self):
        editor = self.main.tabWidget_files.currentWidget()
        index = self.main.tabWidget_files.currentIndex()
        editor.text_edit.redo()
        
        
    #----------------------------------------------------------------------
    @Decorator.requiere_text_mode()
    @Decorator.requiere_open_files()
    def cut(self):
        editor = self.main.tabWidget_files.currentWidget()
        index = self.main.tabWidget_files.currentIndex()
        editor.text_edit.cut()
        
        
    #----------------------------------------------------------------------
    @Decorator.requiere_text_mode()
    @Decorator.requiere_open_files()
    def copy(self):
        editor = self.main.tabWidget_files.currentWidget()
        index = self.main.tabWidget_files.currentIndex()
        editor.text_edit.copy()
        
        
    #----------------------------------------------------------------------
    @Decorator.requiere_text_mode()
    @Decorator.requiere_open_files()
    def paste(self):
        editor = self.main.tabWidget_files.currentWidget()
        index = self.main.tabWidget_files.currentIndex()
        editor.text_edit.paste()
    
    
    #----------------------------------------------------------------------
    @Decorator.requiere_open_files()
    def set_tab_search(self):
        self.main.tabWidget_tools.setCurrentIndex(2)
        self.main.lineEdit_search.setFocus()
        
        
    # Menu Source
    
    #----------------------------------------------------------------------
    @Decorator.requiere_open_files()
    def commentregion(self):
        editor = self.main.tabWidget_files.currentWidget()
        comment_wildcard = "// "
        
        #cursor is a COPY all changes do not affect the QPlainTextEdit's cursor!!!
        cursor = editor.text_edit.textCursor()
        
        text = cursor.selectedText()
        
        if text == "":  #no selected, single line
            start = editor.text_edit.document().findBlock(cursor.selectionStart()).firstLineNumber()
            startPosition = editor.text_edit.document().findBlockByLineNumber(start).position()    
            endPosition = editor.text_edit.document().findBlockByLineNumber(start+1).position() - 1        
            
            cursor.setPosition(startPosition)            
            cursor.setPosition(endPosition, QtGui.QTextCursor.KeepAnchor)
            editor.text_edit.setTextCursor(cursor)
            
        else:
            start = editor.text_edit.document().findBlock(cursor.selectionStart()).firstLineNumber()
            startPosition = editor.text_edit.document().findBlockByLineNumber(start).position()
            
            
            end = editor.text_edit.document().findBlock(cursor.selectionEnd()).firstLineNumber()            
            
            endPosition = editor.text_edit.document().findBlockByLineNumber(end+1).position() - 1        
            
            cursor.setPosition(startPosition)            
            cursor.setPosition(endPosition, QtGui.QTextCursor.KeepAnchor)
            editor.text_edit.setTextCursor(cursor)        
        
        
        cursor = editor.text_edit.textCursor()
        
        start_ = cursor.selectionStart()
        end_ = cursor.selectionEnd()        
                
        selectionEnd = cursor.selectionEnd()
        start = editor.text_edit.document().findBlock(cursor.selectionStart()).firstLineNumber()
        end = editor.text_edit.document().findBlock(cursor.selectionEnd()).firstLineNumber()
        startPosition = editor.text_edit.document().findBlockByLineNumber(start).position()
        
        #init=(start, end)
        #Start a undo block
        cursor.beginEditBlock()
    
        #Move the COPY cursor
        cursor.setPosition(startPosition)
        #Move the QPlainTextEdit Cursor where the COPY cursor IS!
        editor.text_edit.setTextCursor(cursor)
        editor.text_edit.moveCursor(QtGui.QTextCursor.StartOfLine)
        
        for i in comment_wildcard:
            editor.text_edit.moveCursor(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor)
        
        start = editor.text_edit.document().findBlock(cursor.selectionStart()).firstLineNumber()
        
        editor.text_edit.moveCursor(QtGui.QTextCursor.StartOfLine)
        s = editor.text_edit.cursor()
        s.pos()
        for i in xrange(start, end + 1):
            editor.text_edit.textCursor().insertText(comment_wildcard)
            #cursor.insertText(comment_wildcard)
            editor.text_edit.moveCursor(QtGui.QTextCursor.Down)
            editor.text_edit.moveCursor(QtGui.QTextCursor.StartOfLine)
            
        editor.text_edit.moveCursor(QtGui.QTextCursor.EndOfLine)
        
        end_ += (end + 1 - start) * 3
        cursor.setPosition(start_)
        cursor.setPosition(end_, QtGui.QTextCursor.KeepAnchor)
        editor.text_edit.setTextCursor(cursor)        
        
        #End a undo block
        cursor.endEditBlock()
        
        
    #----------------------------------------------------------------------
    @Decorator.requiere_open_files()
    def uncommentregion(self):
        
        editor = self.main.tabWidget_files.currentWidget()
        comment_wildcard = "// "
    
        #cursor is a COPY all changes do not affect the QPlainTextEdit's cursor!!!
        cursor = editor.text_edit.textCursor()

        start_ = cursor.selectionStart()
        end_ = cursor.selectionEnd()         
        
        start = editor.text_edit.document().findBlock(cursor.selectionStart()).firstLineNumber()
        end = editor.text_edit.document().findBlock(cursor.selectionEnd()).firstLineNumber()
        startPosition = editor.text_edit.document().findBlockByLineNumber(start).position()

        #Start a undo block
        cursor.beginEditBlock()
    
        #Move the COPY cursor
        cursor.setPosition(startPosition)
        #Move the QPlainTextEdit Cursor where the COPY cursor IS!
        editor.text_edit.setTextCursor(cursor)
        editor.text_edit.moveCursor(QtGui.QTextCursor.StartOfLine)
        for i in xrange(start, end + 1):
            
            for i in comment_wildcard:
                editor.text_edit.moveCursor(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor)
            
            text = editor.text_edit.textCursor().selectedText()
            if text == comment_wildcard:
                editor.text_edit.textCursor().removeSelectedText()
            elif u'\u2029' in text:
                #\u2029 is the unicode char for \n
                #if there is a newline, rollback the selection made above.
                editor.text_edit.moveCursor(QtGui.QTextCursor.Left, QtGui.QTextCursor.KeepAnchor)
    
            editor.text_edit.moveCursor(QtGui.QTextCursor.Down)
            editor.text_edit.moveCursor(QtGui.QTextCursor.StartOfLine)
            
        end_ -= (end + 1 - start) * 3
        cursor.setPosition(start_)
        cursor.setPosition(end_, QtGui.QTextCursor.KeepAnchor)
        editor.text_edit.setTextCursor(cursor)              
    
        #End a undo block
        cursor.endEditBlock()
        

    # Menu View
        
    #----------------------------------------------------------------------
    def __show_hex_code__(self):
        if getattr(self.get_tab().currentWidget(), "path", False):
            hex_filename = self.get_tab().currentWidget().path.replace(".gpde", ".pde").replace(".pde", ".hex")
        else:
            Dialogs.error_message(self, QtGui.QApplication.translate("Dialogs", "You must compile before."))
            return
        if os.path.isfile(hex_filename):
            self.frame_hex_viewer = HexViewer(self, hex_filename)
            self.frame_hex_viewer.show()    
        else:
            Dialogs.error_message(self, QtGui.QApplication.translate("Dialogs", "You must compile before."))
                    
                
    #----------------------------------------------------------------------
    def __show_stdout__(self):
        self.frame_stdout = PlainOut("Stdout")
        self.frame_stdout.show()
    
    
    # Pinguino
    
    #----------------------------------------------------------------------
    def __show_libmanager__(self):
        self.frame_stdout = LibManager(self)
        self.frame_stdout.show()
        
        
    #----------------------------------------------------------------------
    def __config_paths__(self):
        self.frame_paths = Paths(self)
        self.frame_paths.show()
        
        
    #----------------------------------------------------------------------
    def __show_board_config__(self):
        self.frame_board = BoardConfig(self)
        self.frame_board.show()
        
    #----------------------------------------------------------------------
    @Decorator.requiere_open_files()
    @Decorator.requiere_file_saved()
    def pinguino_compile(self):
        if not self.is_graphical():
            filename = self.get_tab().currentWidget().path
        else:
            filename = self.PinguinoKIT.save_as_pde()
            filename = self.get_tab().currentWidget().path.replace(".gpde", ".pde")
            
        self.set_board()
        reply = Dialogs.confirm_board(self)
    
        if reply == False:
            self.__show_board_config__()
            return
        elif reply == None: return
            
        self.output_ide(QtGui.QApplication.translate("Frame", "compilling: %s")%filename)
        self.output_ide(self.get_description_board())
        
        self.pinguinoAPI.compile_file(filename)
        
        self.main.actionUpload.setEnabled(self.pinguinoAPI.compiled())
        if not self.pinguinoAPI.compiled():
            
            errors_preprocess = self.pinguinoAPI.get_errors_preprocess()
            if errors_preprocess:
                for error in errors_preprocess["preprocess"]:
                    self.output_ide(error)
            
            errors_c = self.pinguinoAPI.get_errors_compiling_c()
            if errors_c:
                self.output_ide(errors_c["complete_message"])
                line_errors = errors_c["line_numbers"]
                for line_error in line_errors:
                    self.highligh_line(line_error, "#ff7f7f")
            
            errors_asm = self.pinguinoAPI.get_errors_compiling_asm()
            if errors_asm:
                for error in errors_asm["error_symbols"]:
                    self.output_ide(error)
            
            errors_linking = self.pinguinoAPI.get_errors_linking()
            if errors_linking:
                for error in errors_linking["linking"]:
                    self.output_ide(error)
                    
            if errors_asm or errors_c:
                if Dialogs.error_while_compiling(self):
                    self.__show_stdout__()
            elif errors_linking:
                if Dialogs.error_while_linking(self):
                    self.__show_stdout__()
            elif errors_preprocess:
                if Dialogs.error_while_preprocess(self):
                    self.__show_stdout__()
                
            else:
                if Dialogs.error_while_unknow(self):
                    self.__show_stdout__()                
                
        else:
            result = self.pinguinoAPI.get_result()
            self.output_ide(QtGui.QApplication.translate("Frame", "compilation done"))
            self.output_ide(result["code_size"])
            self.output_ide(QtGui.QApplication.translate("Frame", "%s seconds process time")%result["time"])
            
            if Dialogs.compilation_done(self):
                self.pinguino_upload()
            
        if self.is_graphical():
            os.remove(filename)
            
        self.main.plainTextEdit_output.appendPlainText(">>> ")
            
        
    #----------------------------------------------------------------------
    @Decorator.requiere_open_files()
    def pinguino_upload(self):
        uploaded, result = self.pinguinoAPI.upload()
        self.output_ide(result)
        if uploaded:
            Dialogs.upload_done(self)
        elif Dialogs.upload_fail(self, result):
            self.pinguino_upload()
            

    # Graphical
    
    #----------------------------------------------------------------------
    def __show_pinguino_code__(self):
        name = getattr(self.get_tab().currentWidget(), "path", "")
        if name: name = " - " + name
        self.frame_pinguino_code = PlainOut(QtGui.QApplication.translate("Dialogs", "Pinguino code"))
        self.frame_pinguino_code.show_text(self.PinguinoKIT.get_pinguino_source_code(), pde=True)
        self.frame_pinguino_code.show()    
        
    #----------------------------------------------------------------------
    def __export_pinguino_code__(self):
        area = self.PinguinoKIT.get_work_area()
        area.export_code_to_pinguino_editor()
                
                
    # Options
    
    #----------------------------------------------------------------------
    def switch_autocomplete(self):
        enable = self.main.actionAutocomplete.isChecked()
        self.configIDE.set("Features", "autocomplete", enable)
        self.configIDE.save_config()
        
        
    #----------------------------------------------------------------------
    def switch_color_theme(self, pinguino_color=True):
        default_pallete = ["toolBar_edit", "toolBar_files", "toolBar_search_replace",
                           "toolBar_undo_redo", "toolBar_pinguino", "toolBar_pinguino",
                           "toolBar_graphical", "toolBar_switch", "statusBar"]
        
        pinguino_pallete = ["dockWidget_output", "dockWidget_tools", "dockWidget_blocks"]
        
        if pinguino_color:
            for element in pinguino_pallete:
                self.PinguinoPallete.set_background_pinguino(getattr(self.main, element))
            for element in default_pallete:
                self.PinguinoPallete.set_default_palette(getattr(self.main, element))
            self.PinguinoPallete.set_background_pinguino(self.main.centralwidget.parent())
            self.main.label_logo.setPixmap(QtGui.QPixmap(":/logo/art/banner.png"))
        else:
            for element in default_pallete + pinguino_pallete:
                self.PinguinoPallete.set_default_palette(getattr(self.main, element))
            self.PinguinoPallete.set_default_palette(self.main.centralwidget.parent())
            self.main.label_logo.setPixmap(QtGui.QPixmap(":/logo/art/banner_blue.png"))
        
        self.configIDE.set("Main", "color_theme", pinguino_color)
        self.main.actionColor_theme.setChecked(pinguino_color)
    
    
    # Help
    
    #----------------------------------------------------------------------
    def show_wiki_docs(self):
        self.frame_wiki_dock = WikiDock()
        self.frame_wiki_dock.show()    
    
        
    #----------------------------------------------------------------------
    def open_web_site(self, url):
        webbrowser.open_new_tab(url)
    
    
    #----------------------------------------------------------------------
    def __show_about__(self):
        self.frame_about = About(self)
        self.frame_about.show()
        
        
    # Tools Files
    
    #----------------------------------------------------------------------
    def jump_dir_files(self, list_widget_item):
        if getattr(list_widget_item, "type_file") == "dir":
            self.__update_path_files__(getattr(list_widget_item, "path_file"))
        if getattr(list_widget_item, "type_file") == "file":
            if getattr(list_widget_item, "path_file").endswith(".pde"):
                self.open_file_from_path(filename=getattr(list_widget_item, "path_file"))
        
        
    #----------------------------------------------------------------------
    def jump_dir_filesg(self, list_widget_item):
        if getattr(list_widget_item, "type_file") == "dir":
            self.__update_graphical_path_files__(getattr(list_widget_item, "path_file"))
        if getattr(list_widget_item, "type_file") == "file":
            if getattr(list_widget_item, "path_file").endswith(".gpde"):
                self.open_file_from_path(filename=getattr(list_widget_item, "path_file"))
                
                
    #----------------------------------------------------------------------
    def change_dir_files(self, to_dir):
        if to_dir == "Examples":
            self.__update_path_files__(os.path.join(os.environ.get("PINGUINO_USER_PATH"), "examples"))
            
        elif to_dir == "Home":
            self.__update_path_files__(QtCore.QDir.home().path())
            
        elif to_dir == "Current file dir":
            editor = self.main.tabWidget_files.currentWidget()
            dir_ = getattr(editor, "path", None)
            if dir_: self.__update_path_files__(os.path.split(dir_)[0])
            
        elif to_dir == "Other...":
            open_dir = Dialogs.set_open_dir(self)
            if open_dir:
                self.__update_path_files__(open_dir)
                
                    
    #----------------------------------------------------------------------
    def change_dir_filesg(self, to_dir):
        if to_dir == "Examples":
            self.__update_graphical_path_files__(os.path.join(os.environ.get("PINGUINO_USER_PATH"), "graphical_examples"))
            
        elif to_dir == "Home":
            self.__update_graphical_path_files__(QtCore.QDir.home().path())
            
        elif to_dir == "Current file dir":
            editor = self.main.tabWidget_files.currentWidget()
            dir_ = getattr(editor, "path", None)
            if dir_: self.__update_graphical_path_files__(os.path.split(dir_)[0])
            
        elif to_dir == "Other...":
            open_dir = Dialogs.set_open_dir(self)
            if open_dir:
                self.__update_graphical_path_files__(open_dir)
                
                
    # Tools Source

    #----------------------------------------------------------------------
    def jump_function(self, model_index):
        column = model_index.column()
        item = self.main.tableWidget_functions.itemFromIndex(model_index).text()
        if column == 2:
            line = item[:item.find("-")]
            self.jump_to_line(int(line))
            

    #----------------------------------------------------------------------
    def jump_directive(self, model_index):
        column = model_index.column()
        item = self.main.tableWidget_directives.itemFromIndex(model_index).text()
        if column == 2:
            line = item
            self.jump_to_line(int(line))
            
            
    #----------------------------------------------------------------------
    def jump_variable(self, model_index):
        column = model_index.column()
        item = self.main.tableWidget_variables.itemFromIndex(model_index).text()
        if column == 1:
            line = item
            self.jump_to_line(int(line))
        
        
    #----------------------------------------------------------------------
    def jump_function_header(self, row):
        item = self.main.tableWidget_functions.item(row, 2).text()
        line = item[:item.find("-")]
        self.jump_to_line(int(line))


    #----------------------------------------------------------------------
    def jump_directive_header(self, row):
        item = self.main.tableWidget_directives.item(row, 2).text()
        line = item
        self.jump_to_line(int(line))
        
        
    #----------------------------------------------------------------------
    def jump_variable_header(self, row):
        item = self.main.tableWidget_variables.item(row, 1).text()
        line = item
        self.jump_to_line(int(line))
    
    
    # Tools Search  
    # see search_replace.py
    
    
    # Widgets
    
    #----------------------------------------------------------------------
    @Decorator.update_toolbar()
    @Decorator.connect_features()
    def tab_changed(self, *args, **kwargs):
        self.main.tabWidget_files.setVisible(self.main.tabWidget_files.count() > 0)
        self.main.frame_logo.setVisible(not self.main.tabWidget_files.count() > 0)
        self.main.actionClose_file.setEnabled(self.main.tabWidget_files.count() > 0)
            
        editor = self.main.tabWidget_files.currentWidget()
        if getattr(editor, "path", None): self.setWindowTitle(Constants.TAB_NAME+" - "+editor.path)
        else: self.setWindowTitle(Constants.TAB_NAME)
        
        index = self.main.tabWidget_files.currentIndex()
        filename = self.main.tabWidget_files.tabText(index)
        if filename.endswith("*"): self.main.actionSave_file.setEnabled(True)
        else: self.main.actionSave_file.setDisabled(True)
        
        self.__update_current_dir_on_files__()
        
        
    #----------------------------------------------------------------------
    def tab_close(self, index):
        editor = self.get_tab().widget(index)
        self.close_file(editor=editor)
    
    
    # Graphical Tool Bar
    
    #----------------------------------------------------------------------
    @Decorator.requiere_open_files()
    def save_screen_image(self):
        editor = self.get_tab().currentWidget()
        scroll_area = editor.scroll_area
        image = QtGui.QPixmap.grabWidget(scroll_area,
                                         QtCore.QRect(0, 0,
                                                      scroll_area.width()-13,
                                                      scroll_area.height()-13))   
        
        filename = self.get_tab().tabText(self.get_tab().currentIndex())
        filename = os.path.splitext(filename)[0] + ".png"
        filename = Dialogs.set_save_image(self, filename)
        if filename: image.save(filename, "png")    
    
    
    #----------------------------------------------------------------------
    def switch_ide_mode(self, graphical):
        self.main.actionSwitch_ide.setChecked(graphical)
        self.main.tabWidget_graphical.setVisible(graphical and self.main.tabWidget_graphical.count()>0)
        self.main.tabWidget_files.setVisible(not graphical and self.main.tabWidget_files.count()>0)
        
        if graphical:
            self.update_actions_for_graphical()
        else:
            self.update_actions_for_text()
        
        self.tab_changed()
        
        
    # Events
        
        
    #----------------------------------------------------------------------
    def __key_press__(self, event):
        editor = self.main.tabWidget_files.currentWidget()
        if self.is_autocomplete_enable():
            editor.text_edit.__keyPressEvent__(event)
        else:
            editor.text_edit.force_keyPressEvent(event)
        
        
    #----------------------------------------------------------------------
    def __drop__(self, event):
        mine = event.mimeData()
        if mine.hasUrls():
            for path in mine.urls():
                self.open_file_from_path(path.path())



