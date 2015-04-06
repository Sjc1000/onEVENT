import os
import datetime

previous = {}

def filechanged(filedir):
	'''filechanged
	Returns true when a files modified timestamp
	params:
		- filedir - The directory of the file, can be a folder.
	If filedir is a folder it will monitor all the files in the folder.
	Non recursive.
	'''
	if os.path.isfile(filedir):
		timechanged = os.path.getmtime(filedir)
		changed = datetime.datetime.fromtimestamp(timechanged)
		if filedir not in previous:
			previous[filedir] = changed
			return (0, 'None')
		if changed != previous[filedir]:
			previous[filedir] = changed
			return (1, filedir, changed)
	else:
		times = []
		for f in os.listdir(filedir):
			timechanged = os.path.getmtime(filedir+f)
			changed = datetime.datetime.fromtimestamp(timechanged)
			times.append(changed)
		
		if filedir not in previous:
			previous[filedir] = times
			return (0, 'None')
		if times != previous[filedir]:
			previous[filedir] = times
			return (1, filedir)
	return (0, 'None')
