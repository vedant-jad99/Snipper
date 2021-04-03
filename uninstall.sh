#!/bin/sh

pip3 uninstall -r requirements.txt

sudo apt autoremove scrot

sudo rm /usr/share/applications/Snipper.desktop

path="$PWD/uninstall-message/message.py"
python3 $path
