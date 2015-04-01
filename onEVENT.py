import json
import os
import imp
import time
import datetime
from subprocess import call

class newevent():
	events = None
	action = None
	delay = None
	repeat = None
	last_data = None
	last_time = None
	alternative = None
	def __init__(self, events, action, repeat, delay, alternative=None):
		self.events = events
		self.action = action
		self.repeat = repeat
		self.delay = delay
		self.alternative = alternative
		
	def run(self, sources):
		output = []
		for event in self.events:
			function = getattr(sources[event['event']], event['event'])
			output.append(function(*event['params']))	
		return output

class onEVENT():
	events = []
	sources = {}
	def __init__(self, eventfolder, eventfile):
		self._eventfolder = eventfolder
		self._eventfile = eventfile
		self.loadevents()
	
	def loadevents(self):
		with open(self._eventfile) as efile:
			edata = json.loads(efile.read())
		for ev in edata:
			if not 'alternative' in ev:
				ev['alternative'] = None
			new_event = newevent(ev['on'], ev['action'], ev['repeat'], ev['delay'], ev['alternative'])
			self.events.append(new_event)
		
		filelist = [f for f in os.listdir(self._eventfolder) if f.endswith('.py')]
		for event in filelist:
			self.sources[event[:event.index('.')]] = imp.load_source(event, self._eventfolder + event )
		return 0
	
	def loadloop(self, timeout=10):
		while True:
			self.loadevents()
			time.sleep(timeout)
		return 1
	
	def checktime(self, event):
		current_time = datetime.datetime.today()
		c = current_time - event.last_time
		check_time = {'seconds': c.seconds, 'minutes': c.seconds // 60, 'hours': c.seconds // 60 // 60}
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
				current_time = datetime.datetime.today()
				if event.last_time != None:
					if self.checktime(event):
						continue

				event_data = event.run(self.sources)
				check_data = [x[0] for x in event_data]
				
				if event.last_data == None:
					self.events[index].last_data = check_data
					continue
				
				if int(event.repeat) == 0 and event.last_data == check_data:
					self.events[index].last_data = [x[0] for x in event_data]
					self.events[index].last_time = current_time
					continue
				
				self.events[index].last_data = [x[0] for x in event_data]
				self.events[index].last_time = current_time
				
				params = []
				output = self.checkoutput(event, event_data)
				
				for p in event_data:
					for i, par in enumerate(p):
						if i == 0:
							continue
						params.append(par)
				if output == 1:
					for command in enumerate(event.action):
						command = [ c.format(*params) for c in command[1] ]
						call(command)
				
				if output == 0 and event.alternative != None:
					for command in enumerate(event.alternative):
						command = [ c.format(*params) for c in command[1] ]
						call(command)
			time.sleep(timeout)
				
				
				


if __name__ == '__main__':
	onEVENT = onEVENT('events/','events.json')
	onEVENT.eventloop()
