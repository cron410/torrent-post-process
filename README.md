torrent-post-process
====================

### relocate.py

Scripts to automatically relocate video files. Detects video type (movie/tv episode)
and moves them to the corresponding directories.

Example:
```
.
|-- downloads
|   |-- my-movie_720p
|   |   |-- downloaded-from-somewhere.txt
|   |   `-- movie.mkv
|   `-- my-show-s01e07.mkv
|-- movies
`-- series
```

Apply `relocate.py ./downloads ./movies ./series` and you will have the following:

```
.
|-- downloads
|   |-- my-movie_720p
|   |   |-- downloaded-from-somewhere.txt
|   |   `-- movie.mkv
|   `-- my-show-s01e07.mkv
|-- movies
|   `-- my\ movie
|       |-- movie.mkv
|       |-- movie.mkv.en.srt.pending
|       `-- movie.mkv.es.srt.pending
`-- series
    `-- my\ show
        `-- s01
            |-- my-show-s01e07.mkv
            |-- my-show-s01e07.mkv.en.srt.pending
            `-- my-show-s01e07.mkv.es.srt.pending
```            
Here, originally downloaded files have been hardlinked (so you can keep seeding!) and flag files
have been created so that subtitles.py can do its magic.

### subtitles.py

Script that scans a video directory looking for missing subtitle flag files (eg "movie.en.srt.pending")
and downloads its subtitles.

On the previous example, running `python subtitles.py ./movies` would produce the following:

```
movies
`-- my\ movie
    |-- movie.mkv
    |-- movie.en.srt
    `-- movie.es.srt
```

### Configuring with transmission

If you have installed Transmission Daemon (`transmission-daemon` package on Debian/Ubuntu), you can
configure it to run a script automatically after a torrent finishes (check out /etc/transmission-daemon/settings.json).

All you should do in this script is build the path to the torrent output file/directory and execute `relocate.py`
and `subtitles.py` in order.

Since the script is run by the transmission user, you can run into file system permission issues. To avoid these, I use
ssh in the transmission script to do the work with my own user:

```
TORRENT_PATH=$TR_TORRENT_DIR/$TR_TORRENT_NAME
ssh pi@localhost sh /home/pi/transmission/post/post.sh \"$TORRENT_PATH\"
```

Note that to do this you should have the corresponding ssh keys already setup. Check out the `examples` subdirectory for
a complete execution script.

### Dependencies and acknowledgements

These scripts require:

   * [guessit](https://pypi.python.org/pypi/guessit/0.2b1)
   * [periscope](https://code.google.com/p/periscope/)

Inspiried in work by [jc89](https://github.com/jc89/). Checkout [this](https://github.com/jc89/torr_flow)
and [this](https://github.com/jc89/rperiscope) project. 
   
