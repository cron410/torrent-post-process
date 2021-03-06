##############################################################################
#
# Scans the video directory for missing subtitle flag files, and tries to
# download the subtitles.
#
# Usage:
# subtitles.py [-h] video_path
#
##############################################################################

import os
import argparse
import periscope
import fs_help
import re
import shutil
from datetime import datetime, timedelta

def parse_args():
	parser = argparse.ArgumentParser(description=
			"""Scans the video directory for missing subtitle flag files,
			and tries to download the subtitles.""")
	parser.add_argument('video_path', type=str,
						help='location where video files are stored')
	return parser.parse_args()

def is_subtitle_missing_flag(fs_path):
	return fs_path.endswith("srt.pending") and len(fs_path.split(".")) >= 5

def subtitle_flags(fs_path):
	return filter(is_subtitle_missing_flag, fs_help.recursive_list_files(fs_path))

def extract_language(flag):
	split = flag.split(".")
	return split[len(split)-3]

def extract_video_file(flag):
	split = flag.split(".")
	return ".".join(split[0:-3])

def rename_subtitle(subtitle_path, language):
	destination = re.sub('.srt$', '.' + language + '.srt', subtitle_path)
	shutil.move(subtitle_path, destination)

def download_subtitle(video_file_path, language):
	print "Downloading subtitle for " + video_file_path + " in " + language
	subtitle = subdl.downloadSubtitle(video_file_path, [language])
	if (subtitle):
		rename_subtitle(subtitle['subtitlepath'], language)
		return True
	else:
		print "Subtitle for " + video_file_path + " not found"
		return False

def flag_expired(subtitle_flag):
	limit_ts = datetime.today() - timedelta(days=3)
	file_ts = datetime.fromtimestamp(os.path.getmtime(subtitle_flag))
	return file_ts < limit_ts

##############################################################################

args = parse_args()
video_path = args.video_path
subdl = periscope.Periscope("/tmp/periscope-cache")

for flag in subtitle_flags(video_path):
	video_file = extract_video_file(flag)
	language = extract_language(flag)
	if download_subtitle(video_file, language) or flag_expired(flag):
		os.remove(flag)