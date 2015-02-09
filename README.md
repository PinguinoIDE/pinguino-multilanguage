pinguino-multilanguage
======================

Multilanguage support for Pinguino IDE


## Generate/update translation files (.ts)

add languange, e.g. Espanish (es):
```shell
$ python gents.py es
```
this must generate/update pinguino_es.ts

add languange, e.g. Brazilian Portuguese (pt_BR):
```shell
$ python gents.py pt_BR
```
this must generate/update pinguino_pt_BR.ts


## Translate files
Now you have your translation files ready to be used with Qt Linguist [you can follow tutorial] (https://qt-project.org/doc/qt-5/linguist-translators.html). Load the `.ts` file, double click entries and type the translation, click the `?` icon to mark them as finished.


## Test translation on Pinguino IDE
In Qt Linguist do `File -> Release` to compile a new .qm file. Copy this file into [multilanguage directory](https://github.com/PinguinoIDE/pinguino-ide/tree/master/multilanguage) and run Pinguino IDE.


## How to add your translations to official Pinguino IDE?
Fork this repository, follow the steps above and do [pull request](https://help.github.com/articles/using-pull-requests/).
Don't forget sign credits.txt with your name.