import os

# recursively list all files (not directories!) under the path
def recursive_list_files(fs_path):
	if (os.path.isfile(fs_path)):
		yield fs_path
	else:
		for dirname, dirnames, filenames in os.walk(fs_path):
			for filename in filenames:
				yield os.path.join(dirname, filename)
