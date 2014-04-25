#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import codecs
import pickle
import logging

from PySide import QtGui, QtCore

from .decorators import Decorator
from .dialogs import Dialogs
from ..tools.files import Files
from ..tools.search_replace import SearchReplace
from ..methods.library_manager import Librarymanager
from ..widgets.output_widget import START


########################################################################
class Methods(SearchReplace):

    #----------------------------------------------------------------------
    #@Decorator.debug_time()
    def open_file_from_path(self, *args, **kwargs):
        filename = kwargs["filename"]
        if self.__check_duplicate_file__(filename): return

        self.update_recents(filename)

        if filename.endswith(".gpde"):
            self.switch_ide_mode(True)
            self.PinguinoKIT.open_file_from_path(filename=filename)
            return
        elif filename.endswith(".pde"):
            self.switch_ide_mode(False)


        self.new_file(filename=filename)
        editor = self.main.tabWidget_files.currentWidget()
        #pde_file = open(path, mode="r")
        pde_file = codecs.open(filename, "r", "utf-8")
        content = "".join(pde_file.readlines())
        pde_file.close()
        editor.text_edit.setPlainText(content)
        setattr(editor, "path", filename)
        setattr(editor, "last_saved", content)
        self.main.tabWidget_files.setTabToolTip(self.main.tabWidget_files.currentIndex(), filename)
        self.main.tabWidget_files.setTabText(self.main.tabWidget_files.currentIndex(), os.path.split(filename)[1])
        self.tab_changed()



    #----------------------------------------------------------------------
    @Decorator.call_later(100)
    #@Decorator.debug_time()
    def open_last_files(self):
        self.recent_files = self.configIDE.get_recents()
        self.update_recents_menu()

        opens = self.configIDE.get_recents_open()
        if not opens: return

        #files = "\n".join(opens)
        #dialogtext = QtGui.QApplication.translate("Dialogs", "Do you want open files of last sesion?")
        #if not Dialogs.confirm_message(self, dialogtext+"\n"+files):
            #return

        self.setCursor(QtCore.Qt.WaitCursor)
        for file_ in opens:
            if os.path.exists(file_):
                try: self.open_file_from_path(filename=file_)
                except: pass

        self.main.actionSwitch_ide.setChecked(file_.endswith(".gpde"))
        self.switch_ide_mode(file_.endswith(".gpde"))
        self.setCursor(QtCore.Qt.ArrowCursor)


    #----------------------------------------------------------------------
    def jump_to_line(self, line):
        self.highligh_line(line, "#DBFFE3")


    #----------------------------------------------------------------------
    @Decorator.requiere_open_files()
    @Decorator.requiere_text_mode()
    def select_block_edit(self):
        editor = self.main.tabWidget_files.currentWidget()
        cursor = editor.text_edit.textCursor()
        prevCursor = editor.text_edit.textCursor()

        text = cursor.selectedText()
        selected = bool(text)

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


        text = cursor.selectedText()

        lines = text.split(u'\u2029')
        firstLine = False
        for line in lines:
            if not line.isspace() and not line == "":
                firstLine = line
                break
        return editor, cursor, prevCursor, selected, firstLine



    #----------------------------------------------------------------------
    @Decorator.requiere_open_files()
    @Decorator.requiere_text_mode()
    def highligh_line(self, line=None, color="#ff0000", text_cursor=None):
        editor = self.main.tabWidget_files.currentWidget()

        if line:
            content = editor.text_edit.toPlainText()
            #line_content = content.split("\n")[line-1]
            content = content.split("\n")[:line]
            position = len("\n".join(content))
            text_cur = editor.text_edit.textCursor()
            text_cur.setPosition(position)
            text_cur.clearSelection()
            editor.text_edit.setTextCursor(text_cur)
        else:
            text_cur = editor.text_edit.textCursor()
            text_doc = editor.text_edit.document()
            text_cur.clearSelection()
            editor.text_edit.setDocument(text_doc)
            editor.text_edit.setTextCursor(text_cur)

        selection = QtGui.QTextEdit.ExtraSelection()
        selection.format.setBackground(QtGui.QColor(color))
        selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
        selection.cursor = editor.text_edit.textCursor()
        editor.text_edit.setExtraSelections(editor.text_edit.extraSelections()+[selection])

        selection.cursor.clearSelection()

        if text_cursor: editor.text_edit.setTextCursor(text_cursor)


    #----------------------------------------------------------------------
    @Decorator.requiere_open_files()
    def clear_highlighted_lines(self):
        editor = self.main.tabWidget_files.currentWidget()
        editor.text_edit.setExtraSelections([])


    #----------------------------------------------------------------------
    def get_tab(self):
        if self.main.actionSwitch_ide.isChecked(): return self.main.tabWidget_graphical
        else: return self.main.tabWidget_files


    #----------------------------------------------------------------------
    def __update_path_files__(self, path):
        Files.update_path_files(path, self.main.listWidget_files, self.main.label_path, exclude=".gpde")


    #----------------------------------------------------------------------
    def __update_graphical_path_files__(self, path):
        Files.update_path_files(path, self.main.listWidget_filesg, self.main.label_pathg, exclude=".pde")


    #----------------------------------------------------------------------
    def __update_current_dir_on_files__(self):
        tab = self.get_tab()
        if tab == self.main.tabWidget_files:
            if self.main.comboBox_files.currentIndex() == 2:
                editor = tab.currentWidget()
                dir_ = getattr(editor, "path", None)
                if dir_: self.__update_path_files__(os.path.split(dir_)[0])

        else:
            if self.main.comboBox_filesg.currentIndex == 2:
                editor = tab.currentWidget()
                dir_ = getattr(editor, "path", None)
                if dir_: self.__update_graphical_path_files__(os.path.split(dir_)[0])


    #----------------------------------------------------------------------
    @Decorator.connect_features()
    def __save_file__(self, *args, **kwargs):
        editor = kwargs.get("editor", self.get_tab())
        content = editor.text_edit.toPlainText()
        #pde_file = open(editor.path, mode="w")
        pde_file = codecs.open(editor.path, "w", "utf-8")
        pde_file.write(content)
        pde_file.close()
        setattr(editor, "last_saved", content)
        self.__text_saved__()


    #----------------------------------------------------------------------
    def __get_name__(self, ext=".pde"):
        index = 1
        name = "untitled-%d" % index + ext
        #filenames = [self.main.tabWidget_files.tabText(i) for i in range(self.main.tabWidget_files.count())]
        filenames = [self.get_tab().tabText(i) for i in range(self.get_tab().count())]
        while name in filenames or name + "*" in filenames:
            index += 1
            name = "untitled-%d" % index + ext
        return name + "*"


    #----------------------------------------------------------------------
    def __text_changed__(self, *args, **kwargs):
        index = self.main.tabWidget_files.currentIndex()
        filename = self.main.tabWidget_files.tabText(index)
        if not filename.endswith("*"):
            self.main.tabWidget_files.setTabText(index, filename+"*")
            self.main.actionSave_file.setEnabled(True)
        self.clear_highlighted_lines()


    #----------------------------------------------------------------------
    def __text_saved__(self, *args, **kwargs):
        index = self.get_tab().currentIndex()
        filename = self.get_tab().tabText(index)
        if filename.endswith("*"):
            self.get_tab().setTabText(index, filename[:-1])
        self.main.actionSave_file.setEnabled(False)


    #----------------------------------------------------------------------
    def __text_can_undo__(self, *args, **kwargs):
        state = not self.main.actionUndo.isEnabled()
        self.main.actionUndo.setEnabled(state)
        editor = self.main.tabWidget_files.currentWidget()
        editor.tool_bar_state["undo"] = state


    #----------------------------------------------------------------------
    def __text_can_redo__(self, *args, **kwargs):
        state = not self.main.actionRedo.isEnabled()
        self.main.actionRedo.setEnabled(state)
        editor = self.main.tabWidget_files.currentWidget()
        editor.tool_bar_state["redo"] = state


    #----------------------------------------------------------------------
    def __text_can_copy__(self, *args, **kwargs):
        state = not self.main.actionCopy.isEnabled()
        self.main.actionCopy.setEnabled(state)
        self.main.actionCut.setEnabled(state)
        editor = self.main.tabWidget_files.currentWidget()
        editor.tool_bar_state["copy"] = state


    #----------------------------------------------------------------------
    def __check_duplicate_file__(self, filename):
        filenames = [getattr(self.get_tab().widget(i), "path", None) for i in range(self.get_tab().count())]
        if filename in filenames:
            Dialogs.file_duplicated(self, filename)
            self.get_tab().setCurrentIndex(filenames.index(filename))
            return True
        return False


    #----------------------------------------------------------------------
    def load_main_config(self):
        if self.configIDE.config("Main", "maximized", True):
            self.showMaximized()

        else:
            pos = self.configIDE.config("Main", "position", "(0, 0)")
            self.move(*eval(pos))

            size = self.configIDE.config("Main", "size", "(1050, 550)")
            self.resize(*eval(size))

        ##self.main.plainTextEdit_output.resize(self.main.plainTextEdit_output.size()+
                                              ##QtCore.QSize(0, self.configIDE.config("Main", "terminal_height", 80))
                                              ##)

        #self.main.dockWidget_output.resize(100, 100)


        #self.configIDE.set("Main", "terminal_height", self.main.plainTextEdit_output.height())


    #----------------------------------------------------------------------
    def get_all_open_files(self):
        opens = []
        tab = self.main.tabWidget_files
        widgets = map(tab.widget, range(tab.count()))
        for widget in widgets:
            path = getattr(widget, "path", False)
            if path: opens.append(path)
        tab = self.main.tabWidget_graphical
        widgets = map(tab.widget, range(tab.count()))
        for widget in widgets:
            path = getattr(widget, "path", False)
            if path: opens.append(path)
        return opens


    #----------------------------------------------------------------------
    def update_recents(self, filename):
        if filename in self.recent_files:
            self.recent_files.remove(filename)
        self.recent_files.insert(0, filename)
        self.recent_files = self.recent_files[:10]

        self.update_recents_menu()


    #----------------------------------------------------------------------
    def update_recents_menu(self):
        self.main.menuRecents.clear()
        for file_ in self.recent_files:
            action = QtGui.QAction(self)
            filename = os.path.split(file_)[1]

            len_ = 40
            if len(file_) > len_:
                file_path_1 = file_[:len_/2]
                file_path_2 = file_[-len_/2:]
                file_path = file_path_1 + "..." + file_path_2
            else: file_path = file_

            if os.path.isfile(file_):
                action.setText(filename+" ("+file_path+")")
                self.connect(action, QtCore.SIGNAL("triggered()"), self.menu_recent_event(file_))
                action.ActionEvent = self.menu_recent_event

                self.main.menuRecents.addAction(action)

        self.main.menuRecents.addSeparator()
        self.main.menuRecents.addAction(QtGui.QApplication.translate("Dialogs", "Clear recent files"), self.clear_recents_menu)

    #----------------------------------------------------------------------
    def clear_recents_menu(self):
        self.main.menuRecents.clear()
        self.main.menuRecents.addSeparator()
        self.main.menuRecents.addAction(QtGui.QApplication.translate("Dialogs", "Clear recent files"), self.clear_recents_menu)
        self.recent_files = []


    #----------------------------------------------------------------------
    def menu_recent_event(self, file_):
        def menu():
            self.open_file_from_path(filename=file_)
        return menu


    ##----------------------------------------------------------------------
    #def update_pinguino_paths(self):
        #user_sdcc_bin = self.configIDE.get_path("sdcc_bin")
        #if user_sdcc_bin: self.pinguinoAPI.P8_BIN = user_sdcc_bin

        #user_gcc_bin = self.configIDE.get_path("gcc_bin")
        #if user_gcc_bin: self.pinguinoAPI.P32_BIN = user_gcc_bin

        #pinguino_source = os.path.join(os.getenv("PINGUINO_USER_PATH"), "source")
        #if pinguino_source: self.pinguinoAPI.SOURCE_DIR = pinguino_source

        #pinguino_8_libs = self.configIDE.get_path("pinguino_8_libs")
        #if pinguino_8_libs: self.pinguinoAPI.P8_DIR = pinguino_8_libs

        #pinguino_32_libs = self.configIDE.get_path("pinguino_32_libs")
        #if pinguino_32_libs: self.pinguinoAPI.P32_DIR = pinguino_32_libs


    #----------------------------------------------------------------------
    def build_statusbar(self):
        #principal status
        self.status_info = QtGui.QLabel()

        #warning status
        self.status_warnnig = QtGui.QLabel()
        self.status_warnnig.setAlignment(QtCore.Qt.AlignRight)
        self.status_warnnig.setStyleSheet("""
        QLabel{
            color: red;
        }
        """)

        self.main.statusBar.addPermanentWidget(self.status_info, 1)
        self.main.statusBar.addPermanentWidget(self.status_warnnig, 2)



    ##----------------------------------------------------------------------
    #def update_namespaces(self):
        #names = Namespaces()
        #names.save_namespaces()

    #----------------------------------------------------------------------
    def write_log(self, *args, **kwargs):

        lines = ""
        for line in args:
            lines += line
            #self.main.plainTextEdit_output.appendPlainText(line)

        for key in kwargs.keys():
            line = key + ": " + kwargs[key]
            lines += line

        #Integration with Shell: print(Lines)
        #self.main.plainTextEdit_output.appendPlainText(lines)
        self.main.plainTextEdit_output.log_output(lines.replace("\n", "\n"+START))

        self.main.plainTextEdit_output.update()

        scroll = self.main.plainTextEdit_output.verticalScrollBar()
        scroll.setValue(scroll.maximum())


    #----------------------------------------------------------------------
    def statusbar_ide(self, status):
        self.status_info.setText(status)

    #----------------------------------------------------------------------
    def statusbar_warnning(self, status):
        self.status_warnnig.setText(status)


    #----------------------------------------------------------------------
    def set_board(self):
        board_name = self.configIDE.config("Board", "board", "Pinguino 2550")
        for board in self.pinguinoAPI._boards_:
            if board.name == board_name:
                self.pinguinoAPI.set_board(board)

        arch = self.configIDE.config("Board", "arch", 8)
        if arch == 8:
            bootloader = self.configIDE.config("Board", "bootloader", "v1_v2")
            if bootloader == "v1_v2":
                self.pinguinoAPI.set_bootloader(self.pinguinoAPI.Boot2)
            else:
                self.pinguinoAPI.set_bootloader(self.pinguinoAPI.Boot4)

        os.environ["PINGUINO_BOARD_ARCH"] = str(arch)


        compiler = self.configIDE.get_path("sdcc_bin"), "sdcc"

        if os.getenv("PINGUINO_OS_NAME") == "windows":
            ext = ".exe"
        elif os.getenv("PINGUINO_OS_NAME") == "linux":
            ext = ""


        if arch == 8:
            compiler = os.path.exists(os.path.join(self.configIDE.get_path("sdcc_bin"), "sdcc" + ext))
            libraries = os.path.exists(self.configIDE.get_path("pinguino_8_libs"))

        elif arch == 32:
            compiler = os.path.exists(os.path.join(self.configIDE.get_path("gcc_bin"), "mips-elf-gcc-4.5.2" + ext))
            libraries = os.path.exists(self.configIDE.get_path("pinguino_32_libs"))

        status = ""
        if not compiler:
            status = QtGui.QApplication.translate("Frame", "Missing compiler for %d-bit") % arch

        elif  not libraries:
            status = QtGui.QApplication.translate("Frame", "Missing libraries for %d-bit") % arch

        if not libraries and not compiler:
            status = QtGui.QApplication.translate("Frame", "Missing libraries and compiler for %d-bit") % arch

        if status:
            self.statusbar_warnning(status)
            os.environ["PINGUINO_CAN_COMPILE"] = "False"
        else:
            os.environ["PINGUINO_CAN_COMPILE"] = "True"



    #----------------------------------------------------------------------
    def get_description_board(self):
        board = self.pinguinoAPI.get_board()
        board_config = "Board: %s\n" % board.name
        board_config += "Proc: %s\n" % board.proc
        board_config += "Arch: %s\n" % board.arch

        if board.arch == 8 and board.bldr == "boot4":
            board_config += "Boootloader: v4\n"
        if board.arch == 8 and board.bldr == "boot2":
            board_config += "Boootloader: v1 & v2\n"

        return board_config


    #----------------------------------------------------------------------
    def get_status_board(self):
        self.set_board()
        board = self.pinguinoAPI.get_board()
        board_config = board.name

        if board.arch == 8 and board.bldr == "boot4":
            board_config += " - Boootloader: v4"
        if board.arch == 8 and board.bldr == "boot2":
            board_config += " - Boootloader: v1 & v2"

        return board_config


    ##----------------------------------------------------------------------
    #def update_user_libs(self):
        #libs = Librarymanager()

        #all_p8 = libs.get_p8_libraries()
        #all_p8 = map(lambda lib:lib["p8"], all_p8)
        #self.pinguinoAPI.USER_P8_LIBS = all_p8

        #all_p32 = libs.get_p32_libraries()
        #all_p32 = map(lambda lib:lib["p32"], all_p32)
        #self.pinguinoAPI.USER_P32_LIBS = all_p32

        #self.pinguinoAPI.USER_PDL = libs.get_pdls()


    #----------------------------------------------------------------------
    def reload_file(self):
        editor = self.main.tabWidget_files.currentWidget()
        filename = getattr(editor, "path", False)
        file_ = codecs.open(filename, "r", "utf-8")
        editor.text_edit.clear()
        editor.text_edit.insertPlainText("".join(file_.readlines()))
        self.save_file()




    #----------------------------------------------------------------------
    def update_reserved_words(self):
        libinstructions = self.pinguinoAPI.read_lib(8)[1]
        name_spaces_8 = map(lambda x:x[0], libinstructions)

        libinstructions = self.pinguinoAPI.read_lib(32)[1]
        name_spaces_32 = map(lambda x:x[0], libinstructions)

        reserved_filename = os.path.join(os.getenv("PINGUINO_USER_PATH"), "reserved.pickle")

        name_spaces_commun = []

        copy_32 = name_spaces_32[:]
        for name in name_spaces_8:
            if name in copy_32:
                name_spaces_8.remove(name)
                name_spaces_32.remove(name)
                name_spaces_commun.append(name)

        namespaces = {"arch8": name_spaces_8, "arch32": name_spaces_32, "all": name_spaces_commun,}
        pickle.dump(namespaces, open(reserved_filename, "w"))

        print("Write on %s" % reserved_filename)


    #----------------------------------------------------------------------
    def update_instaled_reserved_words(self):
        libinstructions = self.pinguinoAPI.read_lib(8, include_default=False)[1]
        name_spaces_8 = map(lambda x:x[0], libinstructions)

        libinstructions = self.pinguinoAPI.read_lib(32, include_default=False)[1]
        name_spaces_32 = map(lambda x:x[0], libinstructions)

        reserved_filename = os.path.join(os.getenv("PINGUINO_USER_PATH"), "reserved.pickle")

        name_spaces_commun = []

        copy_32 = name_spaces_32[:]
        for name in name_spaces_8:
            if name in copy_32:
                name_spaces_8.remove(name)
                name_spaces_32.remove(name)
                name_spaces_commun.append(name)


        olds = pickle.load(open(reserved_filename, "r"))


        namespaces = {"arch8": list(set(name_spaces_8 + olds["arch8"])),
                      "arch32": list(set(name_spaces_32 + olds["arch32"])),
                      "all": list(set(name_spaces_commun + olds["all"])),}

        #pickle.dump(olds, open(reserved_filename, "w"))
        pickle.dump(namespaces, open(reserved_filename, "w"))

        print("Write on %s" % reserved_filename)



    #----------------------------------------------------------------------
    def load_fonts(self):
        #fonts_dir = os.path.join(os.getenv("PINGUINO_INSTALL_PATH"), "ide", "qtgui", "resources", "fonts")
        fonts_dir = os.path.join(os.getenv("PINGUINO_DATA"), "qtgui", "resources", "fonts")
        if not os.path.exists(fonts_dir):
            logging.warning("Missing: "+fonts_dir)
            return

        for dir_font in os.listdir(fonts_dir):
            for ttf in filter(lambda file:file.endswith(".ttf") or file.endswith(".otf"), os.listdir(os.path.join(fonts_dir, dir_font))):
                #print QtGui.QFontDatabase.addApplicationFontFromData(os.path.join(fonts_dir, dir_font, ttf))
                status = QtGui.QFontDatabase.addApplicationFont(os.path.join(fonts_dir, dir_font, ttf))
                if status == -1: logging.warning("Error loading: "+os.path.join(fonts_dir, dir_font, ttf))


    #----------------------------------------------------------------------
    def exapand_editor(self, exapand):

        self.toggle_toolbars(not exapand)
        self.main.dockWidget_output.setVisible(not exapand)
        self.main.actionToolbars.setChecked(not exapand)

        self.main.statusBar.setVisible(not exapand)

        if self.is_graphical():
            self.main.dockWidget_blocks.setVisible(not exapand)
            self.main.dockWidget_tools.setVisible(False)
        else:
            self.main.dockWidget_tools.setVisible(not exapand)
            self.main.dockWidget_blocks.setVisible(False)

    #----------------------------------------------------------------------
    def toggle_toolbars(self, visible):

        if visible == False:
            for toolbar in self.toolbars:
                toolbar.setVisible(visible)

        else:

            self.main.toolBar_switch.setVisible(True)
            self.main.toolBar_files.setVisible(True)
            self.main.toolBar_pinguino.setVisible(True)

            visible = self.is_graphical()

            self.main.toolBar_edit.setVisible(not visible)
            self.main.toolBar_graphical.setVisible(visible)
            self.main.toolBar_search_replace.setVisible(not visible)
            self.main.toolBar_undo_redo.setVisible(not visible)
