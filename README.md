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

#### Configuring with transmission

Check out the `examples` subdirectory for an example Transmission configuration script.

### Dependencies and acknowledgements

These scripts require:

   * [guessit](https://pypi.python.org/pypi/guessit/0.2b1)
   * [periscope](https://code.google.com/p/periscope/)

Inspiried in work by [jc89](https://github.com/jc89/). Checkout [this](https://github.com/jc89/torr_flow)
and [this](https://github.com/jc89/rperiscope) project. 
   
