import time

def getuptime():
	with open('/proc/uptime') as ufile:
		uptime = float(ufile.read().split(' ')[0])
	return uptime

def timetoseconds(time):
	convert = {'days': 60*60*24, 'minutes': 60, 'hours': 60*60, 'seconds': 1}
	timeinseconds = 0
	
	for c in time:
		if c in convert:
			timeinseconds += time[c] * convert[c]
	return timeinseconds

def _between(first, second):
	obj = getuptime()
	first = timetoseconds(first)
	second = timetoseconds(second)
	m, s = divmod(obj, 60)
	h, m = divmod(m, 60)
	return (first < obj < second, '%d:%d:%d' %(h, m, s))

def _is(time):
	obj = getuptime()
	timeinseconds = timetoseconds(time)
	m, s = divmod(obj, 60)
	h, m = divmod(m, 60)
	return (obj == timeinseconds, '%d:%d:%d' %(h, m, s))

def _larger(time):
	obj = getuptime()
	timeinseconds = timetoseconds(time)
	m, s = divmod(obj, 60)
	h, m = divmod(m, 60)
	return (obj > timeinseconds, '%d:%d:%d' %(h, m, s))

def _smaller(time):
	obj = getuptime()
	timeinseconds = timetoseconds(time)
	m, s = divmod(obj, 60)
	h, m = divmod(m, 60)
	return (obj < timeinseconds, '%d:%d:%d' %(h, m, s))


def uptime(function='is', *params):
	'''uptime
	Checks the uptime of the PC
	params:
		- function - can be is, larger, smaller, between
		- params - Usually 1 timeobject, unless its between it will be 2 timeobjects
		
	timeobject
		{'seconds': ammount of seconds, 'minutes': ammount of minutes, 'hours': ammount of hours, 'days': ammount of days}
		You can leave out any of these params.
	'''
	if '_' + function in globals():
		return globals()['_'+function](*params)
	print('Uptime check cant be done, ' + function + ' not defined.')
	return (0, 'None')

if __name__ == '__main__':
	help(uptime)
