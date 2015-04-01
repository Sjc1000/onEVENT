
#/proc/bus/input

def inputdevice(device):
	'''inputdevice
	Checks if a device is plugged in. Things such as mice.
	params:
		- device - The device to check.
	'''
	with open('/proc/bus/input/devices', 'r') as dfile:
		file_data = dfile.read()
	devices = []
	for item in file_data.split('\n\n'):
		data = item.split('\n')
		for i in data:
			if i.startswith('N'):
				d = i[i.index('"')+1:i.index('"', i.index('"') + 1)]
				if d not in devices:
					devices.append(d)

	for d in devices:
		if device in d:
			return (1, d)
	return (0, device)


if __name__ == '__main__':
	help(inputdevice)
