##############################################################################
#
# Usage:
# prueba.py [-h] torrent_path movies_dir series_dir
#
##############################################################################

import os
import guessit
import sys
import argparse


def parse_args():
	parser = argparse.ArgumentParser(description='Process Transmission output')
	parser.add_argument('torrent_path', type=str,
						help='location where transmission downloaded the torrent')
	parser.add_argument('movies_dir', type=str,
						help='directory where movies will be relocated')
	parser.add_argument('series_dir', type=str,
						help='directory where tv episoded will be relocated')
	return parser.parse_args()


def is_video_file(fs_path):
	file_info = guessit.guess_video_info(fs_path)
	return ('mimetype' in file_info) and file_info['mimetype'].startswith("video/")

# recursively list all files (not directories!) under the path
def recursive_list_files(fs_path):
	if (os.path.isfile(fs_path)):
		yield fs_path
	else:
		for dirname, dirnames, filenames in os.walk(fs_path):
			for filename in filenames:
				yield os.path.join(dirname, filename)

# finds all video files located under a directory
def find_video_files(fs_path):
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
def flag_required_subtitles(basename, destination):
	name_no_extension = os.path.splitext(basename)[0]
	es_flag = os.path.join(destination, name_no_extension + ".es.srt.pending")
	en_flag = os.path.join(destination, name_no_extension + ".en.srt.pending")
	open(es_flag, 'w').close()
	open(en_flag, 'w').close()

# Moves the video to the destination file (creating it if necessary),
# and creates missing subtitle flags
def locate(origin, destination):
	if (not os.path.exists(destination)):
		os.makedirs(destination)

	basename = os.path.basename(origin)
	target_file = os.path.join(destination, basename)
	flag_required_subtitles(basename, destination)
	os.link(origin, target_file)

def process_movie_file(file_path, metadata):
	dest = os.path.join(movies_dir, metadata["title"])
	locate (file_path, dest)

def process_episode_file(file_path, metadata):
	dest = os.path.join(series_dir, metadata["series"], "s" + str(metadata["season"]).zfill(2))
	locate (file_path, dest)


##############################################################################

args = parse_args()

torrent_output_path = args.torrent_path
movies_dir = args.movies_dir
series_dir = args.series_dir

process_all_files(torrent_output_path)
