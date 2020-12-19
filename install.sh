#!/bin/sh

sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install python3-tk

pip3 install -r requirements.txt

string='[Desktop Entry]
Version=1.0
Type=Application
Terminal=false
Name=Snipper\n'
path_exec="Exec=bash -c $PWD/run.sh
Icon=/home/thedarkcoder/Desktop/Projects/snipping_tool/assets/Snipper.jpg"

echo "$string$path_exec" > Snipper.desktop

sudo mv Snipper.desktop /usr/share/applications/Snipper.desktop

string_run="#!/bin/sh\n\n"
path="path=$PWD/main.py\n"
next_line='/usr/bin/env python3 "$path"'

echo "$string_run$path$next_line" > run.sh