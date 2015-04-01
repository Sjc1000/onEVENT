import os
import time

def get_cpu():
	HZ = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
	with open('/proc/stat', 'r') as pfile:
		previous = pfile.read().split('\n')[0].split(' ')[4]
	time.sleep(1)
	with open('/proc/stat', 'r') as pfile:
		current = pfile.read().split('\n')[0].split(' ')[4]
	cpu = (int(current) - int(previous) ) / (1 * HZ ) * 100
	return cpu

def _is(cpu):
	gcpu = get_cpu()
	return (int(cpu) == gcpu, gcpu)

def _larger(cpu):
	gcpu = get_cpu()
	return (int(cpu) < gcpu, gcpu)

def _smaller(cpu):
	gcpu = get_cpu()
	return (int(cpu) > gcpu, gcpu)

def _between(lower, higher):
	cpu = get_cpu()
	return (int(lower) < cpu < int(higher), cpu )

def cpu(function='is', *params):
	'''cpu
	An event to check the cpu
	params
		- function - can be is, larger, smaller, between
		- params - all are single numbers, but if you use between you need a lower, higher as params.
	'''
	if '_' + function in globals():
		f = globals()['_' + function](*params)
		return f
	return (0, 'None')

if __name__ == '__main__':
	help(cpu)
