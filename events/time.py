from time import localtime, strftime

def _is(format, time):
	current = strftime(format, localtime())
	if current == time:
		return (1, strftime('%H:%M:%S', localtime()))
	return (0, 'Not time')

def _later(format, time):
	current = strftime(format, localtime())
	try:
		time = int(time)
		current = int(current)
	except:
		print('Unable to convert time to int. Please only specify numbers.')
		raise
	if current > time:
		return (1, strftime('%H:%M:%S', localtime()))
	return (0, 'Not later')

def _earlier(format, time):
	current = strftime(format, localtime())
	try:
		time = int(time)
		current = int(current)
	except:
		print('Unable to convert time to int. Please only specify numbers.')
		raise
	if current < time:
		return (1, strftime('%H:%M:%S', localtime()))
	return (0, 'Not ealer.')


def _between(format, first, second):
	current = strftime(format, localtime())
	try:
		first = int(first)
		second = int(second)
		current = int(current)
	except:
		print('Unable to convert time to int. Please only specify numbers.')
		raise
	if first < current < second:
		return (1, strftime('%H:%M:%S', localtime()))
	return (0, 'Not between.')

def time(function='is', *params):
	'''time
	Checks the time. python's time module is used for formatting. It can be found in the python docs.
	params:
		- function - Can be is, between, earlier, later.
		- format - The format of the time
		- time - The time you wish to check against
		- ( optional ) - second time, use in between function.
	'''
	if '_'+function in globals():
		return globals()['_'+function](*params)
	return (0, 'None')

if __name__ == '__main__':
	help(time)
