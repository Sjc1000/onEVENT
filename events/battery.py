import os
#/sys/class/power_supply/BAT0

def getbatteryinfo():
	batfolder = ''
	battery = {}
	for folder in os.listdir('/sys/class/power_supply'):
		if 'BAT' in folder:
			batfolder = '/sys/class/power_supply/' + folder + '/'
			break

	_files = os.listdir(batfolder)
	for f in _files:
		if os.path.isfile(batfolder+f):
			with open(batfolder + f, 'r') as tfile:
				battery[f] = tfile.read().split('\n')[0]
	return battery

def getbatterylevel():
	battery = getbatteryinfo()
	current = battery['charge_now']
	full = battery['charge_full']
	capacity = battery['capacity']
	perc = round((int(current) / int(full) * 100 ))
	if perc > 100:
		perc = 100
	return perc

def _is(level):
	return (getbatterylevel() == int(level), getbatterylevel())

def _between(first, second):
	return (int(first) < getbatterylevel() < int(second), getbatterylevel())

def _smaller(amount):
	return (int(amount) > getbatterylevel(), getbatterylevel())

def _larger(amount):
	return (int(amount) < getbatterylevel(), getbatterylevel())

def _charging():
	battery = getbatteryinfo()
	return (battery['status'] == 'Charging' or battery['status'] == 'Full', getbatterylevel())

def _full():
	battery = getbatteryinfo()
	return (battery['status'] == 'Full', getbatterylevel())

def battery(function, *params):
	'''battery
	params:
		- function - can be is, between, smaller, larger, charging, full.
		- params - params to be passed to each function.
	'''
	getbatterylevel()
	if '_' + function in globals():
		return globals()['_'+function](*params)
	return (0, 'None')

if __name__ == '__main__':
	help(battery)
