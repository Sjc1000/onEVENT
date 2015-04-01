import os

def exists(directory):
	'''exists
	Returns true if a directory exists
	params:
		- directory - The directory to check
	'''
	return (os.path.isdir(directory), directory)


if __name__ == '__main__':
	help(exists)
