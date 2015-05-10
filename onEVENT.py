#!/urs/bin/env python3
import json
import ast
import os
import imp
import time
import datetime
import threading
from subprocess import call, DEVNULL
import argparse
import sys
import socketserver
from cprint import cprint
import eventparser

"""
    onEVENT is an event based automation system for Linux made by Sjc1000 
                ( Steven J. Core )
            Copyright © 2015, Steven J. Core.
    
    onEVENT is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


__version__ = '1.3.0'


def timestamp():
    time_object = time.localtime(time.time())
    return '[{:0>2}:{:0>2}:{:0>2}]'.format(time_object[3],
              time_object[4],time_object[5])


class NewEvent():
    """newevent
    A class for handling all the event data. With a few methods. 
    Such as run and reload.
    """
    events = None
    action = None
    delay = None
    repeat = None
    last_data = None
    last_time = None
    alternative = None
    def __init__(self, events, action, repeat, delay, alternative=None,
                 id=None, iterate=0):
        self.events = events
        self.action = ast.literal_eval(action)
        self.repeat = repeat
        self.delay = ast.literal_eval(delay)
        if alternative is not None:
            self.alternative = ast.literal_eval(alternative)
        self.id = id
        self.iterate = iterate
        
    def run(self, sources):
        """run
        Runs the event file.
        Loading from the sources dictionary.
        """
        output = []
        for event in self.events:
            function = getattr(sources[event['event']], event['event'])
            output.append(function(*event['params']))    
        return output


class onEVENT():
    """onEVENT class
    The base system of onEVENT.
    """
    events = []
    sources = {}
    def __init__(self, eventfolder, eventfile):
        """__init__
        params:
            - eventfolder - The folder where all the events are stored.
            - eventfile - The event json file to load from.
        """
        self._eventfolder = eventfolder
        self._eventfile = eventfile
        self.loadevents()
        
        if attemptreload:
            reload_thread = threading.Thread(target=self.reloadloop)
            reload_thread.daemon = True
            reload_thread.start()
        
        if verbose:
            cprint('[.green] Now watching events!', '[.purple]' + timestamp())
        
        if server:
            self.server = socketserver.server(host, port, local)
            connect_thread = threading.Thread(
                target=self.server.listen)
            connect_thread.daemon = True
            connect_thread.start()
    
    def reloadloop(self):
        """reloadloop
        The reload loop. Started in a different thread.
        This attemps to reload event data while the program is in use.
        It will only do this if you run onEVENT -r
        """
        while True:
            time.sleep(60)
            self.loadevents()
        return None
    
    def loadevents(self):
        """loadevents
        Loads all the events and creates event classes.
        """
        self.events = []
        with open(self._eventfile) as efile:
            edata = eventparser.parse(efile.read())

        if verbose:
            cprint(' Reading event file and creating event classes.',
                   '[.purple]' + timestamp())
        for index, ev in enumerate(edata):
            if not 'alternative' in ev:
                ev['alternative'] = None
            if not 'iterate' in ev:
                ev['iterate'] = 0
            new_event = NewEvent(
                ev['on'], ev['action'], ev['repeat'], 
                ev['delay'], ev['alternative'], index, ev['iterate'])
            
            if verbose:
                cprint('\t[.blue]Creating event class > [.green]' + 
                       ', '.join([x['event'] for x in ev['on']]),
                       '[.purple]' + timestamp())
            self.events.append(new_event)
        
        filelist = [f for f in os.listdir(self._eventfolder) if 
                    f.endswith('.py')]
        if verbose:
            cprint(' Importing event source files.',
                   '[.purple]' + timestamp())
        for event in filelist:
            if verbose:
                cprint('\t[.blue]Importing [.green]' + event, '[.purple]' + 
                       timestamp(), '\n[.red]')
            self.sources[event[:event.index('.')]] = imp.load_source(
                event, self._eventfolder + event )
        return None
    
    def checktime(self, event):
        """checktime
        Checks the events last time against the current time.
        This returns 1 if the event can be run.
        params:
            - event - The event to check.
        """
        current_time = time.time()
        c = current_time - event.last_time
        m, s = divmod(c, 60)
        h, m = divmod(m, 60)
        check_time = {'seconds': s, 'minutes': m, 'hours': h}
        for d in event.delay:
            if check_time[d] > int(event.delay[d]):
                return False
        return True
    
    def checkoutput(self, event, event_data):
        """checkoutput
        Checks the output of an event against the last event data.
        """
        for index, response in enumerate(event_data):
            if int(response) != int(event.events[index]['result']):
                return False
        return True
    
    def eventloop(self, timeout=1):
        """eventloop
        The main event loop. Runs all the events.
        """
        while True:
            for index, event in enumerate(self.events):
                event_thread = threading.Thread(
                    target=self.callevent,
                    args=(index, event))
                event_thread.daemon = True
                event_thread.start()
            time.sleep(timeout)
        return None
    
    def callevent(self, index, event):
        """callevent
        Calls the event.
        params:
            - index - The index of the event.
            - event - The event itself.
        """
        current_time = time.time()
         
        if event.last_time is not None:
            if self.checktime(event):
                return None

        self.events[index].last_time = current_time
        try:
            event_data = event.run(self.sources)
        except Exception as Error:
            cprint(' [.red]Error raised in event - ' + 
                   ', '.join([x['event'] for x in event.events]) + 
                   ' - ' + str(Error), '[.purple]' + timestamp())
            return None

        check_data = [x[0] for x in event_data]
        
        if int(event_data[0][0]) == -1 and verbose:
            cprint(' [.red]Error > ' + event.events[0]['event'], 
                   '[.purple]' + timestamp())
            return None
        
        if event.last_data is None:
            self.events[index].last_data = check_data
        
        if int(event.repeat) == 0 and event.last_data == check_data:
            return None
        if verbose:
            space1 = 15-len(event.events[0]['event'])
            space = 25-len(', '.join(event.events[0]['params'])[:24])
            cprint(' [.blue]' + event.events[0]['event'][:13] + ' '*space1 + 
                   '| [.green]' + 
                   ', '.join(event.events[0]['params'])[:24] + 
                   ' ' * space + '[.blue]|[.purple][.bold] ' + 
                   str(check_data), '[.purple]' + timestamp())
        if server:
            e = event.events
            for a, b in zip(enumerate(e), event_data):
                i, a = a
                a['output'] = b
                e[i] = a
            self.server.send(json.dumps(e))
                
        params = []
        output = self.checkoutput(event, check_data)
        
        self.events[index].last_data = check_data
        
        for p in event_data:
            for i, par in enumerate(p):
                if i == 0:
                    continue
                params.append(par)
        
        if output:
            if isinstance(params[0], list) and event.iterate:
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
                    call(command, stdout=DEVNULL)
    
        if output is False and event.alternative is not None:
            for command in enumerate(event.alternative):
                command = [c.format(*params) for c in command[1]]
                call(command, stdout=DEVNULL)
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='onEVENT event based automation system for Linux.',
        prog='onEVENT')
    parser.add_argument(
        '--file', 
        help='The location of the file where your events are.',
        default='eventfile')
    parser.add_argument(
        '--folder', 
        help='The folder where all the events are stored.',
        default='events/')
    parser.add_argument(
        '-v', '--verbose',
        help='Verbose mode. Displays the output of everything',
        action='store_true')
    parser.add_argument(
        '-r', '--reload',
        help='Makes the program attempt to reload info from the event '
        'file every 60 seconds. Will not add new events just reloads '
        'current event info.',
        action='store_true')
    parser.add_argument(
        '-V', action='version', 
        version='%(prog)s is currently version ' + str(__version__))
    parser.add_argument(
        '-T', '--timeout', help='The timeout between the checking the '
        'events.',
        default=1, type=int)
    parser.add_argument(
        '-s', '--server', help='Turns this into a server.',
        action='store_true', 
        default=False)
    parser.add_argument(
        '-o', '--host', help='The host for this to run on.', 
        type=str, default='')
    parser.add_argument(
        '-p', '--port', help='The port for this to run on.', type=int, 
        default=9987)
    parser.add_argument(
        '-l', '--local', action='store_true', help='Run it locally or '
        'online.', 
        default=False)
    parser.add_argument(
        '-e', '--showall', help='Shows every action that onEVENT makes.',
        action='store_true', default=False)

    args = parser.parse_args()
    verbose = args.verbose
    eventfile = args.file
    attemptreload = args.reload


    if args.server:
        server = True
        host = args.host
        port = args.port
        local = args.local
    else:
        server = False

    try:
        onEVENT = onEVENT(args.folder,args.file)
        onEVENT.eventloop(args.timeout)
    except KeyboardInterrupt:
        print('')
        cprint('[.red]Shutting down.')
        if server:
            onEVENT.server.shutdown()
