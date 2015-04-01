import os
filelist = []

def newfile(folder):
	'''newfile
	Returns true if there is a new file in a folder
	params:
		- folder - The folder to check
	'''
	global filelist
	newlist = os.listdir(folder)
	difference = [f for f in newlist if f not in filelist]
	filelist = newlist
	if len(difference):
		return (1, ','.join(difference), folder)
	return (0, 'No new')

if __name__ == '__main__':
	help(newfile)
