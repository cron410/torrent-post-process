#! /bin/bash

##############################################################################
#
# Example transmission post processing script.
# This script triggers the video files relocation and then looks for the
# subtitles.
#
# Configure your /etc/transmission-daemon/settings.json to run this.
#
# Depends on Transmission setting $TR_TORRENT_DIR and $TR_TORRENT_NAME
# environment variables.
#
##############################################################################


# CONFIGURATION
RELOCATE_SCRIPT=/home/pi/transmission/post-torrent.py
SUBTITLES_SCRIPT=/home/pi/transmission/subtitles.py
VIDEO_PATH=/mnt/PASSPORT/video

TORRENT_PATH=$TR_TORRENT_DIR/$TR_TORRENT_NAME
MOVIES_PATH=$VIDEO_PATH/pelis
SERIES_PATH=$VIDEO_PATH/series

python $RELOCATE_SCRIPT "$TORRENT_PATH" "$MOVIES_PATH" "$SERIES_PATH"
python $SUBTITLES_SCRIPT "$VIDEO_PATH"