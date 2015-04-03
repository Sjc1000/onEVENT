import os
#/sys/class/power_supply/BAT0

def getbatteryinfo():
	batfolder = ''
	battery = {}
	for folder in os.listdir('/sys/class/power_supply'):
		if 'BAT' in folder:
			batfolder = '/sys/class/power_supply/' + folder
			break

	with open(batfolder + '/uevent') as ufile:
		battery_info = ufile.read()
	
	for item in battery_info.split('\n'):
		if item == '':
			continue
		battery[item.split('=')[0]] = item.split('=')[1]
	return battery

def getbatterylevel():
	battery = getbatteryinfo()
	full = battery['POWER_SUPPLY_CHARGE_FULL']
	current = battery['POWER_SUPPLY_CHARGE_NOW']
	cap = battery['POWER_SUPPLY_CAPACITY']
	perc = round((float(full) / float(current)) * float(cap))
	return int(perc)

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
	return (battery['POWER_SUPPLY_STATUS'] == 'Charging' or battery['POWER_SUPPLY_STATUS'] == 'Full', getbatterylevel())

def _full():
	battery = getbatteryinfo()
	return (battery['POWER_SUPPLY_STATUS'] == 'Full', getbatterylevel())

def battery(function, *params):
	'''battery
	params:
		- function - can be is, between, smaller, larger, charging, full.
		- params - params to be passed to each function.
	'''
	if '_' + function in globals():
		return globals()['_'+function](*params)
	return (0, 'None')


if __name__ == '__main__':
	help(battery)
