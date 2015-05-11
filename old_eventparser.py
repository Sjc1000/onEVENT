#!/usr/bin/env python3

"""
A parser for my events.
Reads the info from event file into python.
"""


example = '''
battery(full) = 1 & battery(charging) = 0:
    repeat: 0
    delay: {seconds: 0}
    action: ["notify-send", "Battery", "Battery is full"]
    
battery(charging) = 1:
    repeat: 0
    delay: {seconds: 0}
    action: ["notify-send", "Battery", "Battery is charging"]
'''

def parse(data):
    output = []
    index = -1
    for line in data.split('\n'):
        if line == '':
            continue
        if any(line.startswith(l) for l in [' ', '\t']) is False:
            output.append({'on': None, 'repeat': None, 'delay': None, 
                          'action': None, 'alternative': None, 'iterate': 
                           None})
            index += 1
            events = [x.strip() for x in line.replace(':','').split('&')]
            params = [x[x.index('(')+1: x.index(')')].split(',') 
                      for x in events]
            results = [int(x.split('=')[1].strip()) for x in events]
            eventnames = [x[:x.index('(')] for x in events]
            joined = [{'event':x[0], 'params': x[1], 'result': x[2]} for x 
                     in zip(eventnames, params, results)]
            output[index]['on'] = joined
        else:
            line = line.strip().split(':')
            key = line[0].strip()
            value = ':'.join(line[1:]).strip()
            if key == '' or value == '':
                continue
            output[index][key] = value
    return output

