#! /bin/python

import os
import guessit
import sys

# reads the path where transmission downloaded
# the torrent from the system environment
def transmission_output():
	key = 'TR_TORRENT_NAME'
	if (key in os.environ):
		path = os.environ[key]
		if (os.path.exists(path)):
			return path
		else:
			raise Exception("Transmission output dir does not exist")
	else:
		raise Exception("Transmission output environment variable not set")

def is_video_file(fs_path):
	file_info = guessit.guess_video_info(fs_path)
	return ('mimetype' in file_info) and file_info['mimetype'].startswith("video/")

# recursively list all files (not directories!) under the path
def recursive_list_files(fs_path):
	for dirname, dirnames, filenames in os.walk(fs_path):
		for filename in filenames:
			yield os.path.join(dirname, filename)

# recursively finds all video files under a file directory
def find_video_files(fs_path):
	if (os.path.isfile(fs_path) and is_video_file(fs_path)):
		return fs_path
	elif (os.path.isdir(fs_path)):
		all_files = recursive_list_files(fs_path)
		return filter(is_video_file, all_files)

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

def process_movie_file(file_path, metadata):
	print "Movie!"

def process_episode_file(file_path, metadata):
	print "Episode!"

