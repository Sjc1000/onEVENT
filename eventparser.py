#!/usr/bin/env python3

"""
Parse the events.
Requires PyYaml.
"""

import yaml

def parse(data):
    p = yaml.load(data)
    output = []
    for item in p:
        obj = {'on': None, 'repeat': None, 'action': None, 'delay': None, 
                'alternative': None, 'iterate': 0}
        obj['delay'] = item['onEVENT']['delay']
        obj['repeat'] = item['onEVENT']['repeat']
        obj['action'] = [x['action'] for x in item['onEVENT']['do']]
        events = [list(y.keys())[0] for y in item['onEVENT']['when']]
        more = [x[events[i]] for i, x in enumerate(item['onEVENT']['when'])]
        ev = []
        for i, e in enumerate(events):
            ev.append({'event': e, 'params': more[i]['params'], 'result': more[i]['result']})
        obj['on'] = ev
        
        if 'alternative' in item['onEVENT']:
            obj['alternative'] = [x['action'] for x in 
                                  item['onEVENT']['alternative']]
        #if 'iterate' in item['onEVENT']:
        try:
            obj['iterate'] = item['onEVENT']['iterate'] 
        except KeyError:
            obj['iterate'] = 0
        output.append(obj)
    return output
