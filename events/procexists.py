import subprocess

def procexists(process):
	'''procexists
	Checks if a process exists
	params:
		- process - The name of the process to search for.
	
	returns:
		- pid - A list of PID's found for the process, if there are more than 1.
	'''
	proc = subprocess.Popen(['ps', '-e'], stdout=subprocess.PIPE)
	grep = subprocess.Popen(['grep', '.*' + process + '.*'], stdin=proc.stdout, stdout=subprocess.PIPE)
	try:
		processes = grep.communicate()[0].decode('utf-8').split('\n')
	except AttributeError:
		return (0, 'None')
	if len(processes) -1:
		pid = [i.split(' ')[1] for i in processes if i != '']
		return (1,) + tuple(pid)
	return (0, 'None')


if __name__ == '__main__':
	help(procexists)
