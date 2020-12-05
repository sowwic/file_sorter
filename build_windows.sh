#!/bin/bash  
APP_NAME="file_sorter"
MAIN_FILE_PATH=file_sorter/main.py
SITE_PACKAGES_PATH=.env/Lib/site-packages
CONFIG_FILE="config.ini;."
RES_FOLDER="res/;."
ICON_PATH=res/images/icon.ico

py -3 -m PyInstaller --onedir --noconsole \
--icon $ICON_PATH \
--paths $SITE_PACKAGES_PATH \
--add-data=$CONFIG_FILE \
-n $APP_NAME \
$MAIN_FILE_PATH

$SHELL 
