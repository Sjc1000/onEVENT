def lidclosed():
	'''lidclosed
	Returns true is the lid is closed. False if not.
	'''
	with open('/proc/acpi/button/lid/LID0/state', 'r') as sfile:
		state = sfile.read().split(':')[1].strip()
	if state == 'open':
		return (0, 'open')
	return (1, 'closed')
	
