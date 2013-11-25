torrent-post-process
====================

Scripts to automatically relocate video files. Detects video type (movie/tv episode)
and moves them to the corresponding directories.

## Relocate.py

Example:
.
|-- downloads
|   |-- my-movie_720p
|   |   |-- downloaded-from-somewhere.txt
|   |   `-- movie.mkv
|   `-- my-show-s01e07.mkv
|-- movies
`-- series


Apply `relocate.py ./downloads ./movies ./series` and you will have the following:

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
            
Here, originally downloaded files have been hardlinked (so you can keep seeding!) and flag files
have been created so that subtitles.py can do its magic.
