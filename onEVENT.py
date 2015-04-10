import json
import os
import imp
import time
import datetime
import threading
from subprocess import call, DEVNULL
from pprint import pprint, colors as c
import argparse
import sys

__version__ = '2.1.0'

class newevent():
	events = None
	action = None
	delay = None
	repeat = None
	last_data = None
	last_time = None
	alternative = None
	def __init__(self, events, action, repeat, delay, alternative=None, id=None):
		self.events = events
		self.action = action
		self.repeat = repeat
		self.delay = delay
		self.alternative = alternative
		self.id = id
		
	def run(self, sources):
		output = []
		for event in self.events:
			function = getattr(sources[event['event']], event['event'])
			output.append(function(*event['params']))	
		return output
	
	def reload(self):
		with open(eventfile, 'r') as efolder:
			data = efolder.read()
		obj = json.loads(data)
		self.repeat = obj[self.id]['repeat']
		self.delay = obj[self.id]['delay']
		self.events = obj[self.id]['on']
		self.action = obj[self.id]['action']
		if self.alternative != None:
			self.alternatice = obj[self.id]['alternative']
		return 0

class onEVENT():
	events = []
	sources = {}
	def __init__(self, eventfolder, eventfile):
		self._eventfolder = eventfolder
		self._eventfile = eventfile
		self.loadevents()
		
		if attemptreload:
			reload_thread = threading.Thread(target=self.reloadloop)
			reload_thread.daemon = True
			reload_thread.start()
		
		if verbose:
			pprint('Now watching events.')
	
	def reloadloop(self):
		while True:
			for event in self.events:
				event.reload()
			time.sleep(60)
		return 0
	
	def loadevents(self):
		with open(self._eventfile) as efile:
			edata = json.loads(efile.read())
		if verbose:
			pprint('Reading event file and creating event classes.')
		for index, ev in enumerate(edata):
			if not 'alternative' in ev:
				ev['alternative'] = None
			new_event = newevent(ev['on'], ev['action'], ev['repeat'], ev['delay'], ev['alternative'], index)
			self.events.append(new_event)
		
		filelist = [f for f in os.listdir(self._eventfolder) if f.endswith('.py')]
		if verbose:
			pprint('Importing event source files.')
		for event in filelist:
			self.sources[event[:event.index('.')]] = imp.load_source(event, self._eventfolder + event )
		return 0
	
	def checktime(self, event):
		current_time = time.time()
		c = current_time - event.last_time
		m, s = divmod(c, 60)
		h, m = divmod(m, 60)
		check_time = {'seconds': s, 'minutes': m, 'hours': h}
		for d in event.delay:
			if check_time[d] < int(event.delay[d]):
				return 1
		return 0
	
	def checkoutput(self, event, event_data):
		for index, response in enumerate(event_data):
			if response[0] != int(event.events[index]['result']):
				return 0
		return 1
	
	def eventloop(self, timeout=1):
		while True:
			for index, event in enumerate(self.events):
				event_thread = threading.Thread(target=self.callevent, args=(index, event))
				event_thread.daemon = True
				event_thread.start()
			time.sleep(timeout)
	
	def callevent(self, index, event):
		current_time = time.time()
		 
		if event.last_time != None:
			if self.checktime(event):
				return 0
		else:
			self.events[index].last_time = current_time
			return 0
		
		self.events[index].last_time = current_time
		
		event_data = event.run(self.sources)
		check_data = [x[0] for x in event_data]
		
		
		if event.last_data == None:
			self.events[index].last_data = check_data
				
		if int(event.repeat) == 0 and event.last_data == check_data:
			return 0
		if verbose:
			space1 = 15-len(event.events[0]['event'])
			space = 25-len(', '.join(event.events[0]['params'])[:24])
			pprint( c['blue'] + '[ ' + c['green'] + event.events[0]['event'][:13] + c['blue'] + ' '*space1 + '| ' + c['red'] + ', '.join(event.events[0]['params'])[:24] + ' ' * space + c['blue'] + '| ' + c['green'] + str(check_data) + c['blue'] + ' ]')
		params = []
		output = self.checkoutput(event, event_data)
		
		self.events[index].last_data = check_data
		
		for p in event_data:
			for i, par in enumerate(p):
				if i == 0:
					continue
				params.append(par)
		if output:
			if isinstance(params[0], list):
				for data in params[0]:
					for command in enumerate(event.action):
						if isinstance(data, dict):
							command = [c.format(**data) for c in command[1]]
						else:
							command = [c.format(*data) for c in command[1]]
						call(command, stdout=DEVNULL)
			else:
				for command in enumerate(event.action):
					command = [c.format(*params) for c in command[1]]
					print( command )
					call(command, stdout=DEVNULL)
	
		if not output and event.alternative != None:
			for command in enumerate(event.alternative):
				command = [c.format(*params) for c in command[1]]
				call(command, stdout=DEVNULL)
		return 0

parser = argparse.ArgumentParser(description='onEVENT event based system for the Linux terminal.', prog='onEVENT')
parser.add_argument('--file', help='The location of the file where your events are.', default='events.json')
parser.add_argument('--folder', help='The folder where all the events are stored.', default='events/')
parser.add_argument('-v', '--verbose', help='Verbose mode. Displays the output of everything', action='store_true')
parser.add_argument('-r', '--reload', help='Makes the program attempt to reload info from the event file every 60 seconds. Will not add new events just reloads current event info.', action='store_true')
parser.add_argument('-V', action='version', version='%(prog)s is currently version ' + str(__version__))
parser.add_argument('-T', '--timeout', help='The timeout between the checking the events.', default=1, type=int)

args = parser.parse_args()
verbose = args.verbose
eventfile = args.file
attemptreload = args.reload

if __name__ == '__main__':
	onEVENT = onEVENT(args.folder,args.file)
	onEVENT.eventloop(args.timeout)
