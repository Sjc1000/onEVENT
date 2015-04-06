import os
directory = '/sys/class/backlight/intel_backlight/'

def get():
	brightness = {}
	clist = os.listdir(directory)
	for cfile in clist:
		if os.path.isfile(directory+cfile):
			with open(directory+cfile, 'r') as fhandle:
				brightness[cfile] = fhandle.read().split('\n')[0]
	return brightness

def _is(value):
	br = get()
	m = int(br['max_brightness'])
	cur = int(br['actual_brightness'])
	return (value == ( cur / m * 100 ), ( cur / m * 100 ))

def _between(lower, higher):
	br = get()
	m = int(br['max_brightness'])
	cur = int(br['actual_brightness'])
	return (int(lower) < (cur / m * 100 ) < int(higher), (cur / m * 100))

def _higher(value):
	br = get()
	m = int(br['max_brightness'])
	cur = int(br['actual_brightness'])
	return ((cur / m * 100 ) > int(value), (cur / m * 100))

def _lower(value):
	br = get()
	m = int(br['max_brightness'])
	cur = int(br['actual_brightness'])
	return ((cur / m * 100 ) < int(value), (cur / m * 100))

def brightness(function, *params):
	if '_'+function in globals():
		return globals()['_'+function](*params)
	return (0, 'Function not defined')
