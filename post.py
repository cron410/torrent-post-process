#
# Use: python post.py <torrent_output_path> <movies_dir> <series_dir>
#

import os
import guessit
import shutil
import sys

torrent_output_path = "./input"
movies_dir = "./movies"
series_dir = "./series"

def is_video_file(fs_path):
	file_info = guessit.guess_video_info(fs_path)
	return ('mimetype' in file_info) and file_info['mimetype'].startswith("video/")

# recursively list all files (not directories!) under the path
def recursive_list_files(fs_path):
	for dirname, dirnames, filenames in os.walk(fs_path):
		for filename in filenames:
			yield os.path.join(dirname, filename)

# finds all video files located under a directory
def find_video_files(fs_path):
	if (os.path.isfile(fs_path) and is_video_file(fs_path)):
		return fs_path
	elif (os.path.isdir(fs_path)):
		all_files = recursive_list_files(fs_path)
		return filter(is_video_file, all_files)

# 
# recursively transverses the directory, detecting video files:
#
# - caregorizing them by type (movies/series)
# - relocates them in their corresponding directory
# - creates empty flag files for missing subtitles
#
def process_all_files(fs_path):
	undecided = []
	for f in find_video_files(fs_path):
		metadata = guessit.guess_video_info(f, info = "filename")
		if (metadata["type"] == "movie"):
			process_movie_file(f, metadata)
		elif (metadata["type"] == "episode"):
			process_episode_file(f, metadata)
		else:
			undecided.append(f)
	if (undecided):
		print "Unable to detect video type for: " + str(undecided)

# Extracts the base filename from file_pat and creates
# a missing subtitle flag (eg: "movie.en.srt.pending")
# in the destination directory
def flag_required_subtitles(file_path, destination):
	file_name = os.path.splitext(os.path.basename(file_path))[0]
	es_flag = os.path.join(destination, file_name + ".es.srt.pending")
	en_flag = os.path.join(destination, file_name + ".en.srt.pending")
	open(es_flag, 'w').close()
	open(en_flag, 'w').close()

# Moves the video to the destination file (creating it if necessary),
# and creates missing subtitle flags
def locate(origin, destination):
	if (not os.path.exists(destination)):
		os.makedirs(destination)
	flag_required_subtitles(origin, destination)
	shutil.move(origin, destination)


def process_movie_file(file_path, metadata):
	file_name = os.path.splitext(file_path)[0]
	dest = os.path.join(movies_dir, metadata["title"])
	locate (file_path, dest)

def process_episode_file(file_path, metadata):
	dest = os.path.join(series_dir, metadata["series"], "s" + str(metadata["season"]).zfill(2))
	locate (file_path, dest)

process_all_files(torrent_output_path)