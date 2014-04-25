#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import codecs
import shutil
import logging
#from ConfigParser import RawConfigParser

from PySide import QtGui, QtCore

from .methods.backgrounds import BackgroundPallete
from .events.events import PinguinoEvents
from .methods.decorators import Decorator
from .methods.dialogs import Dialogs
from .methods.config import Config
from .code_editor.autocomplete_icons import CompleteIcons
from .widgets.output_widget import PinguinoTerminal
from .methods.widgets_features import PrettyFeatures
from ..gide.app.graphical import GraphicalIDE
from ..frames.main import Ui_PinguinoIDE
from ..pinguino_api.pinguino import Pinguino, AllBoards
from ..pinguino_api.pinguino_config import PinguinoConfig


########################################################################
class PinguinoIDE(QtGui.QMainWindow, PinguinoEvents):

    #@Decorator.debug_time()
    def __init__(self, splash_write):
        super(PinguinoIDE, self).__init__()

        QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForName("UTF-8"))
        QtCore.QTextCodec.setCodecForLocale(QtCore.QTextCodec.codecForName("UTF-8"))
        QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName("UTF-8"))

        self.main = Ui_PinguinoIDE()
        self.main.setupUi(self)
        self.reload_toolbar_icons()

        #set_environ_vars()
        #self.check_user_files()
        splash_write(QtGui.QApplication.translate("Splash", "Setting enviroment values"))
        PinguinoConfig.set_environ_vars()
        splash_write(QtGui.QApplication.translate("Splash", "Checking user files"))
        PinguinoConfig.check_user_files()

        splash_write(QtGui.QApplication.translate("Splash", "Loading Pinguino API"))
        self.pinguinoAPI = Pinguino()
        self.pinguinoAPI._boards_ = AllBoards
        splash_write(QtGui.QApplication.translate("Splash", "Loading configuration object"))
        self.configIDE = Config()
        splash_write(QtGui.QApplication.translate("Splash", "Loading graphical mode"))
        self.PinguinoKIT = GraphicalIDE(self)
        self.main.tabWidget_graphical.setVisible(False)
        self.main.dockWidget_blocks.setVisible(False)

        splash_write(QtGui.QApplication.translate("Splash", "Loading icons"))
        self.ICONS = CompleteIcons()

        #self.update_pinguino_paths()
        #self.update_user_libs()
        splash_write(QtGui.QApplication.translate("Splash", "Linking paths for libraries and compilers"))
        PinguinoConfig.update_pinguino_paths(self.configIDE, self.pinguinoAPI)
        PinguinoConfig.update_pinguino_extra_options(self.configIDE, self.pinguinoAPI)
        splash_write(QtGui.QApplication.translate("Splash", "Searching user libraries"))
        PinguinoConfig.update_user_libs(self.pinguinoAPI)
        self.pinguinoAPI.set_os_variables()

        self.setWindowTitle(os.getenv("NAME")+" "+os.getenv("VERSION"))

        splash_write(QtGui.QApplication.translate("Splash", "Opening last files"))
        self.open_last_files()

        splash_write(QtGui.QApplication.translate("Splash", "Starting widgets features"))
        self.init_widgets()
        splash_write(QtGui.QApplication.translate("Splash", "Building status bar"))
        self.build_statusbar()
        splash_write(QtGui.QApplication.translate("Splash", "Building Python Shell"))
        self.build_output()

        splash_write(QtGui.QApplication.translate("Splash", "Overwriting stylesheets"))
        self.set_styleSheet()

        #timer events
        splash_write(QtGui.QApplication.translate("Splash", "Starting timers"))
        self.update_functions()
        self.update_directives()
        self.update_variables()
        self.update_autocompleter()
        self.check_external_changes()

        splash_write(QtGui.QApplication.translate("Splash", "Loading examples"))
        self.__update_path_files__(os.path.join(os.getenv("PINGUINO_USER_PATH"), "examples"))
        self.__update_graphical_path_files__(os.path.join(os.getenv("PINGUINO_USER_PATH"), "graphical_examples"))

        splash_write(QtGui.QApplication.translate("Splash", "Loading boards configuration"))
        self.set_board()
        self.statusbar_ide(self.get_status_board())

        splash_write(QtGui.QApplication.translate("Splash", "Loading configuration"))
        self.load_main_config()
        splash_write(QtGui.QApplication.translate("Splash", "Connecting events"))
        self.connect_events()

        os_name = os.getenv("PINGUINO_OS_NAME")
        if os_name == "windows":
            os.environ["PATH"] = os.environ["PATH"] + ";" + self.configIDE.get_path("sdcc_bin")

        elif os_name == "linux":
            os.environ["LD_LIBRARY_PATH"]="/usr/lib32:/usr/lib:/usr/lib64"


        splash_write(QtGui.QApplication.translate("Splash", "Welcome to %s %s")%(os.getenv("NAME"), os.getenv("VERSION")))



    ##----------------------------------------------------------------------
    #def __str__(self):
        #return " ".join([os.getenv("NAME"), os.getenv("VERSION")])


    #----------------------------------------------------------------------
    @Decorator.debug_time()
    def test_method(self):
        """This method is called from Pinguino's terminal with the command: test_method()"""


    #----------------------------------------------------------------------
    def init_widgets(self):
        self.main.tabWidget_files.setVisible(False)
        self.main.toolBar_graphical.setVisible(False)

        self.main.tabWidget_tools.setCurrentIndex(0)
        self.main.tabWidget_blocks_tools.setCurrentIndex(0)

        PrettyFeatures.LineEdit_default_text(self.main.lineEdit_search, QtGui.QApplication.translate("Frame", "Search..."))
        PrettyFeatures.LineEdit_default_text(self.main.lineEdit_replace, QtGui.QApplication.translate("Frame", "Replace..."))
        PrettyFeatures.LineEdit_default_text(self.main.lineEdit_blocks_search, QtGui.QApplication.translate("Frame", "Search block..."))


        self.toolbars = [self.main.toolBar_edit,
                    self.main.toolBar_files,
                    self.main.toolBar_graphical,
                    self.main.toolBar_pinguino,
                    self.main.toolBar_search_replace,
                    self.main.toolBar_switch,
                    self.main.toolBar_undo_redo,
                    ]

        for toolbar in self.toolbars:
            toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)  #explicit IconOnly for windows
            #toolbar.setIconSize(QtCore.QSize(24, 24))
            toolbar.setIconSize(QtCore.QSize(32, 32))
            #toolbar.setIconSize(QtCore.QSize(48, 48))


    #----------------------------------------------------------------------
    def set_styleSheet(self):
        self.load_fonts()

        self.PinguinoPallete = BackgroundPallete()
        self.PinguinoPallete.save_palette(self.main.centralwidget.parent())
        self.switch_color_theme(self.configIDE.config("Main", "color_theme", True))

        bg_color = self.configIDE.config("Styles", "background_color", "#FFFFFF")
        alternate_bg_color = self.configIDE.config("Styles", "alternate_background_color", "#DDE8FF")

        self.main.tableWidget_functions.setStyleSheet("""
        QTableWidget {
            background-color: %s;
            alternate-background-color: %s;
        }
        """%(bg_color, alternate_bg_color))

        self.main.tableWidget_directives.setStyleSheet("""
        QTableWidget {
            background-color: %s;
            alternate-background-color: %s;
        }
        """%(bg_color, alternate_bg_color))

        self.main.tableWidget_variables.setStyleSheet("""
        QTableWidget {
            background-color: %s;
            alternate-background-color: %s;
        }
        """%(bg_color, alternate_bg_color))


        #Global CSS styles
        self.setStyleSheet("""
        font-family: ubuntu regular;
        font-weight: normal;

        """)

        self.main.groupBox_replace.setStyleSheet("""
        QGroupBox{
            font-family: ubuntu regular;
            font-weight: bold;
        }
        """)

        self.main.groupBox_search.setStyleSheet("""
        QGroupBox{
            font-family: ubuntu regular;
            font-weight: bold;
        }
        """)

        #Python shell CSS styles
        self.main.plainTextEdit_output.setStyleSheet("""
        QPlainTextEdit {
            background-color: #333;
            color: #FFFFFF;
            font-family: ubuntu mono;
            font-weight: normal;
            font-size: 11pt;
        }

        """)



    #----------------------------------------------------------------------
    def build_output(self):
        self.main.actionAutocomplete.setChecked(self.configIDE.config("Features", "autocomplete", True))
        self.main.plainTextEdit_output = PinguinoTerminal(self.main.dockWidgetContents_2)

        class DevTools(object):
            update_reserved = self.update_reserved_words
            update_installed_reserved = self.update_instaled_reserved_words

            functions = ["update_reserved",
                         "update_installed_reserved",

                         ]

        self.main.plainTextEdit_output.set_extra_args(**{"pinguino_main": self,
                                                         "devmode": DevTools(),
                                                         "test_method": self.test_method,})
        self.main.gridLayout_3.addWidget(self.main.plainTextEdit_output, 0, 0, 1, 1)

    #----------------------------------------------------------------------
    def is_graphical(self):
        return self.main.actionSwitch_ide.isChecked()

    #----------------------------------------------------------------------
    def is_widget(self):
        tab = self.get_tab()
        editor = tab.currentWidget()
        if editor is None: return False
        return getattr(editor, "is_widget", False)

    #----------------------------------------------------------------------
    def is_autocomplete_enable(self):
        return self.main.actionAutocomplete.isChecked()

    #----------------------------------------------------------------------
    def update_actions_for_text(self):
        normal = False
        #self.main.menuGraphical.setEnabled(normal)
        self.main.actionExport_code_to_editor.setEnabled(normal)
        self.main.actionView_Pinguino_code.setEnabled(normal)
        self.main.actionInsert_Block.setEnabled(normal)

        self.main.actionComment_out_region.setEnabled(not normal)
        self.main.actionComment_Uncomment_region.setEnabled(not normal)
        self.main.actionRedo.setEnabled(not normal)
        self.main.actionUndo.setEnabled(not normal)
        self.main.actionCut.setEnabled(not normal)
        self.main.actionCopy.setEnabled(not normal)
        self.main.actionPaste.setEnabled(not normal)
        self.main.actionSearch.setEnabled(not normal)
        self.main.actionSearch_and_replace.setEnabled(not normal)
        self.main.dockWidget_blocks.setVisible(normal)
        self.main.dockWidget_tools.setVisible(not normal)
        self.main.toolBar_search_replace.setVisible(not normal)
        self.main.toolBar_edit.setVisible(not normal)
        self.main.toolBar_graphical.setVisible(normal)
        self.main.toolBar_undo_redo.setVisible(not normal)

        #self.configIDE.set("Features", "terminal_on_graphical", self.main.dockWidget_output.isVisible())
        self.main.dockWidget_output.setVisible(self.configIDE.config("Features", "terminal_on_text", True))
        self.main.actionPython_shell.setChecked(self.configIDE.config("Features", "terminal_on_text", True))
        self.configIDE.save_config()


    #----------------------------------------------------------------------
    def update_actions_for_graphical(self):
        normal = True
        #self.main.menuGraphical.setEnabled(normal)
        self.main.actionExport_code_to_editor.setEnabled(normal)
        self.main.actionView_Pinguino_code.setEnabled(normal)
        self.main.actionInsert_Block.setEnabled(normal)

        self.main.actionRedo.setEnabled(not normal)
        self.main.actionComment_out_region.setEnabled(not normal)
        self.main.actionComment_Uncomment_region.setEnabled(not normal)
        self.main.actionUndo.setEnabled(not normal)
        self.main.actionCut.setEnabled(not normal)
        self.main.actionCopy.setEnabled(not normal)
        self.main.actionPaste.setEnabled(not normal)
        self.main.actionSearch.setEnabled(not normal)
        self.main.actionSearch_and_replace.setEnabled(not normal)
        self.main.dockWidget_blocks.setVisible(normal)
        self.main.dockWidget_tools.setVisible(not normal)
        self.main.toolBar_search_replace.setVisible(not normal)
        self.main.toolBar_edit.setVisible(not normal)
        self.main.toolBar_graphical.setVisible(normal)
        self.main.toolBar_undo_redo.setVisible(not normal)

        #self.configIDE.set("Features", "terminal_on_text", self.main.dockWidget_output.isVisible())
        self.main.dockWidget_output.setVisible(self.configIDE.config("Features", "terminal_on_graphical", False))
        self.main.actionPython_shell.setChecked(self.configIDE.config("Features", "terminal_on_graphical", False))
        self.configIDE.save_config()

    #----------------------------------------------------------------------
    def reload_toolbar_icons(self):

        icons_toolbar = [
                         (self.main.actionNew_file, "new_file"),
                         (self.main.actionOpen_file, "open_file"),
                         (self.main.actionSave_file, "save_file"),

                         (self.main.actionUndo, "undo"),
                         (self.main.actionRedo, "redo"),
                         (self.main.actionCut, "cut"),
                         (self.main.actionCopy, "copy"),
                         (self.main.actionPaste, "paste"),

                         (self.main.actionSearch, "search"),
                         (self.main.actionSearch_and_replace, "replace"),

                         (self.main.actionSelect_board, "board"),
                         (self.main.actionCompile, "compile"),
                         (self.main.actionUpload, "download"),

                         (self.main.actionSave_image, "save_image"),
                         #(self.main.actionSwitch_ide, ""),

                        ]

        for action, icon_name in icons_toolbar:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/toolbar/toolbar/%s.svg"%icon_name), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            action.setIcon(icon)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/toolbar/toolbar/switch_to_text.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap(":/toolbar/toolbar/switch_to_graphical.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.main.actionSwitch_ide.setIcon(icon)