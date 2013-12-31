#! /bin/bash
 
######################################################################################
#
# Triggers file relocation and subtitle downloading.
# Assumes the running user has read permission over torrent files and
# write permission over target directory.
#
# Usage: ./post-torrent.sh <torrent-output-path>
#
#
# TO USE WITH TRANSMISSION:
#
# Executing the scripts directly from transmission post processing script can be
# complicated if transmission is run by a different user (default).
#
# I suggest using ssh from transmission script to execute this one with your regular user.
# This way you can keep your directories owners/permissions untouched :-)
#
# Example transmission script:
# 
#	TORRENT_PATH=$TR_TORRENT_DIR/$TR_TORRENT_NAME
#	ssh pi@localhost sh /home/pi/transmission/post/post-torrent.sh \"$TORRENT_PATH\"
#
#
######################################################################################
 
RELOCATE_SCRIPT=/home/pi/transmission/git/relocate.py
SUBTITLES_SCRIPT=/home/pi/transmission/git/subtitles.py

VIDEO_PATH=/mnt/PASSPORT/video 
MOVIES_PATH=$VIDEO_PATH/pelis
SERIES_PATH=$VIDEO_PATH/series
 
LOGFILE=/home/pi/transmission/post/post.log
 
echo "Moving files form $1 to $VIDEO_PATH" >> $LOGFILE
python $RELOCATE_SCRIPT "$1" "$MOVIES_PATH" "$SERIES_PATH"
 
echo "Downloading subtitles" >> $LOGFILE
python $SUBTITLES_SCRIPT "$VIDEO_PATH"
 
echo "Notifying via email" >> $LOGFILE
basename "$1" | mail -s "Transmission download finished" you@email.com
 
echo "==========================================================" >> $LOGFILE