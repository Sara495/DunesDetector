#!/bin/bash

#grass_path= grass76 ---config path 
#export command is used to export a variable or function 
#to the environment of all the child processes running in the current shell.
# path to GRASS binaries and libraries:

export GISBASE=/usr/lib/grass76
export GRASS_VERSION="76"

foldin=$(jq -r '.parameters | .[].foldin' /home/user/.local/share/QGIS/QGIS3/profiles/default/python/plugins/dunes_detector/pythonScripts/config.json)
roi=$(jq -r '.parameters | .[].roi' /home/user/.local/share/QGIS/QGIS3/profiles/default/python/plugins/dunes_detector/pythonScripts/config.json)
resolution=$(jq -r '.parameters | .[].resolution' /home/user/.local/share/QGIS/QGIS3/profiles/default/python/plugins/dunes_detector/pythonScripts/config.json)
echo $roi
echo $foldin
echo $resolution
#generate GISRCRC
MYGISDBASE=$HOME/grassdata
grass76 -c -e  $roi  $HOME/grassdata/mylocation
grass76 -c -e -text $HOME/grassdata/mylocation/mymapset
#grass76 -c -e -text /media/sf_sharedosgeo/UAE/study_area/egypt_utm36N.shp  $HOME/grassdata/mylocation
#grass76 -c -e -text $HOME/grassdata/mylocation/mymapset
MYLOC=mylocation
MYMAPSET=mymapset

# Set the global grassrc file to individual file name
MYGISRC="$HOME/.grassrc.$GRASS_VERSION.$$"
#to append text to a file you use >>
#To overwrite the data currently in that file, you use >
echo "GISDBASE: $MYGISDBASE" > "$MYGISRC"
echo "LOCATION_NAME: $MYLOC" >> "$MYGISRC"
echo "MAPSET: $MYMAPSET" >> "$MYGISRC"
echo "GRASS_GUI: text" >> "$MYGISRC"
 
# path to GRASS settings file
export GISRC=$MYGISRC
export GRASS_PYTHON=python
export GRASS_MESSAGE_FORMAT=plain
export GRASS_TRUECOLOR=TRUE
export GRASS_TRANSPARENT=TRUE
export GRASS_PNG_AUTO_WRITE=TRUE
export GRASS_GNUPLOT='gnuplot -persist'
export GRASS_WIDTH=640
export GRASS_HEIGHT=480
export GRASS_HTML_BROWSER=firefox
export GRASS_PAGER=cat

# #For the temporal modules
export TGISDB_DRIVER=sqlite
export TGISDB_DATABASE=$MYGISDBASE/$MYLOC/PERMANENT/tgis/sqlite.db


# system vars
export PATH="$GISBASE/bin:$GISBASE/scripts:$PATH"
export LD_LIBRARY_PATH="$GISBASE/lib"
export GRASS_LD_LIBRARY_PATH="$LD_LIBRARY_PATH"
export PYTHONPATH="$GISBASE/etc/python:$PYTHONPATH"
export MANPATH=$MANPATH:$GISBASE/man
export GRASS_ADDON_BASE=$HOME/.grass7/addons


cd '/home/user/.local/share/QGIS/QGIS3/profiles/default/python/plugins/dunes_detector/pythonScripts/'


GRASSBIN=$HOME/bin/grass76 python S2_preprocessing.py $foldin $roi $resolution
#GRASSBIN=$HOME/bin/grass76 python S2_preprocessing.py "/home/user/Desktop/UAE/rawdataEGYPT/" "/home/user/Desktop/UAE/study_area/egypt_utm36N.shp" 10
