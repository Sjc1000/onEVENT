import subprocess

def getram():
	output = {}
	with open('/proc/meminfo', 'r') as mfile:
		data = mfile.read()
	for line in data.split('\n'):
		if line == '':
			continue
		name = line.split(':')[0].strip()
		value = line.split(':')[1].strip().replace('kB', '')
		output[name] = int(value)
	return output

def ram(function, *params):
	if '_'+function in globals():
		return globals()['_'+function](*params)
	return 0

ram('is', 'test')
