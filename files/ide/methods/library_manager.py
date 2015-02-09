#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys

# Python3 compatibility
if os.getenv("PINGUINO_PYTHON") is "3":
    #Python3
    from configparser import ConfigParser
else:
    #Python2
    from ConfigParser import RawConfigParser
import logging
import shutil


########################################################################
class Librarymanager(object):

    #----------------------------------------------------------------------
    def __init__(self):
        self.libraries = self.get_libraries()


    #----------------------------------------------------------------------
    def get_libraries(self):
        path = os.path.join(os.getenv("PINGUINO_USERLIBS_PATH"), "libraries")
        if not os.path.exists(path): return []
        dirs = os.listdir(path)

        libraries = []
        for dir_ in dirs:
            #if os.path.isdir(os.path.join(path, dir_)):
            try:
                config = self.parser_to_dict(os.path.join(path, dir_, "config"))
            except:
                shutil.rmtree(os.path.join(path, dir_))
                if os.path.exists(os.path.join(os.path.join(os.getenv("PINGUINO_USERLIBS_PATH"), "examples"), dir_)):
                    shutil.rmtree(os.path.join(os.path.join(os.getenv("PINGUINO_USERLIBS_PATH"), "examples"), dir_))
                if os.path.exists(os.path.join(os.path.join(os.getenv("PINGUINO_USERLIBS_PATH"), "blocks"), dir_)):
                    shutil.rmtree(os.path.join(os.path.join(os.getenv("PINGUINO_USERLIBS_PATH"), "blocks"), dir_))
                continue
            dict_ = {}

            if config.get("active", "False") == "False": continue

            dict_["pdl"] = os.path.join(path, dir_, "lib", "pdl")

            if os.path.isdir(os.path.join(path, dir_, "lib", "p8")):
                dict_["p8"] = os.path.join(path, dir_, "lib", "p8")

            if os.path.isdir(os.path.join(path, dir_, "lib", "p32")):
                dict_["p32"] = os.path.join(path, dir_, "lib", "p32")

            #if os.path.isdir(os.path.join(path, dir_, "lib", "examples")):
                #dict_["examples"] = (config["name"], os.path.join(path, dir_, "lib", "examples"))

            libraries.append(dict_)

        return libraries


    #----------------------------------------------------------------------
    def get_p8_libraries(self):
        return filter(lambda lib:lib.get("p8", False), self.libraries)


    #----------------------------------------------------------------------
    def get_p32_libraries(self):
        return filter(lambda lib:lib.get("p32", False), self.libraries)


    #----------------------------------------------------------------------
    def get_pdls(self):
        #_list_pdls = map(lambda lib:map(lambda pdl_file:os.path.join(lib["pdl"], pdl_file) , os.listdir(lib["pdl"])), self.libraries)

        list_pdls = []
        for lib in self.libraries:
            if os.path.exists(lib["pdl"]):
                list_pdls.extend(map(lambda pdl_file:os.path.join(lib["pdl"], pdl_file), os.listdir(lib["pdl"])))
            else:
                logging.warning("Missing: "+lib["pdl"])

        #pdl = []
        #for list_pdl in list_pdls:
            #pdl.extend(list_pdl)
        return list_pdls

    #----------------------------------------------------------------------
    def parser_to_dict(self, filename):
        parser = RawConfigParser()
        parser.readfp(open(filename, "r"))
        dict_ = {}
        options = parser.options("LIB")
        for option in options: dict_[option] = parser.get("LIB", option)
        return dict_
