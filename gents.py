#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import os
import sys

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
        
        
file_ts = "pinguino_%s.ts"%lang

kalam = open("project.pro", "w")
kalam.write("SOURCES = " + " ".join(python_files) + "\n")
kalam.write("FORMS = " + " ".join(ui_files) + "\n")
kalam.write("TRANSLATIONS = " + file_ts + "\n")
kalam.close()

time.sleep(0.1)  #important delay
exist = os.path.exists(file_ts)
os.system("pyside-lupdate project.pro")
#os.remove("project.pro")

if exist:
    print("pinguino_%s.ts updated"%lang)
else:
    print("pinguino_%s.ts generated"%lang)
    
