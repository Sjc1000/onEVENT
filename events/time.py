from time import localtime, strftime

def time(format, t, action='is'):
	'''time
	Checks the time. python's time module is used for formatting. It can be found in the python docs.
	params:
		- format - The format of the time
		- time - The time you wish to check against
		- action ( planned feature ) - Will be is, larger, smaller, between
	'''
	local = localtime()
	if strftime(format, local) == t:
		return (1, strftime('%I:%M:%S', local))
	return (0, 'None')

if __name__ == '__main__':
	help(time)
