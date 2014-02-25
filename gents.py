#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import os
import sys

if len(sys.argv) == 1:
    print("Missing locale name\n")
    print("e.g.: python gents.py de")
    print("      python gents.py de_DE\n")
    print("A locale name usually has the form ‘ll_CC’. Here ‘ll’ is an ISO 639 two-letter language code,"
          "and ‘CC’ is an ISO 3166 two-letter country code. For example, for German in Germany, ll is de, "
          "and CC is DE. You find a list of the language codes in appendix Language Codes and a list of the "
          "country codes in appendix Country Codes.\n")
    
    print("ISO 639 reference: https://www.gnu.org/software/gettext/manual/html_node/Usual-Language-Codes.html#Usual-Language-Codes")
    print("ISO 3166reference: https://www.gnu.org/software/gettext/manual/html_node/Country-Codes.html#Country-Codes")
    print("\n")
    print("Locale Names: https://www.gnu.org/software/gettext/manual/html_node/Locale-Names.html")
    sys.exit()

elif len(sys.argv) > 2:
    print("One (and only one) argument is requiered.")
    sys.exit()
    
lang = sys.argv[1]
    

files = []
for root, dirnames, filenames in os.walk("files"):
    filenames = filter(lambda filename: filename.endswith(".py") or filename.endswith(".ui"), filenames)
    for filename in filenames:
        files.append(os.path.join(root, filename))
        
python_files = []
for file_ in files:
    if file_.endswith(".py"):
        python_files.append(file_)

ui_files = []
for file_ in files:
    if file_.endswith(".ui"):
        ui_files.append(file_)
          
#exclude compiled files
for ui_file in ui_files:
    py_file = ui_file.replace(".ui", ".py")
    if py_file in python_files:
        python_files.pop(python_files.index(py_file))
        #print("exclude: " + py_file)

file_ts = "pinguino_%s.ts"%lang

kalam = open("project.pro", "w")
kalam.write("SOURCES = " + " ".join(python_files) + "\n")
kalam.write("FORMS = " + " ".join(ui_files) + "\n")
kalam.write("TRANSLATIONS = " + file_ts + "\n")
kalam.close()

time.sleep(0.1)  #important delay
exist = os.path.exists(file_ts)
os.system("pyside-lupdate -verbose project.pro")
#os.remove("project.pro")
