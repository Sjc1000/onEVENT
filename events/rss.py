import urllib.request
import os
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

septags = {'1.0': 'entry', '2.0': 'item'}

class htmlStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.strict = False
		self.convert_charrefs = True
		self.data = []
		self.prepend = []
	
	def handle_data(self, data):
		self.data.append(data)
	
	def get_data(self):
		return ''.join(self.data)

def strip(html):
	s = htmlStripper()
	if html == None:
		return None
	s.feed(html)
	return s.get_data()

def main():
	'''main
	Checks if the RSS previous folder exists and if not, creates it.
	'''
	if not os.path.exists('previous/RSS'):
		os.makedirs('previous/RSS')
	return 0

def download(url):
	request = urllib.request.urlopen(url)
	data = request.read()
	try:
		decoded = data.decode('utf-8')
	except UnicodeDecodeError:
		return 1
	return decoded

def parse1(channel):
	output = {'items': []}
	for i, child in enumerate(channel):
		name = child.tag[child.tag.index('}')+1:]
		if name == 'entry':
			obj = {}
			for x in child:
				if x.tag[child.tag.index('}')+1:] == 'author':
					obj['author'] = strip(x[0].text)
				else:
					obj[x.tag[child.tag.index('}')+1:]] = strip(x.text)
			output['items'].append(obj)
		else:
			output[name] = child.text
	return output

def parser(channel):
	output = {'items': []}
	for index, item in enumerate(channel[0]):
		if item.tag == 'item':
			output['items'].append({x.tag: strip(x.text) for x in item})
		else:
			output[item.tag] = item.text
	if len(output['items']) == 0:
		return parse1(channel)
	return output

def rss(rss_url):
	try:
		data = download(rss_url)
	except:
		return (0, 'None')
	root = ET.fromstring(data)
	current = parser(root)
	title = current['title']
	if os.path.exists('previous/RSS/' + title):
		with open('previous/RSS/' + title, 'r') as pfile:
			d = pfile.read()
			r = ET.fromstring(d)
			previous = parser(r)
	else:
		previous = current
		with open('previous/RSS/' + title, 'w') as pfile:
			pfile.write(data)
		return (0, 'None')
	
	difference = [x for x in current['items'] if x not in previous['items']]
	newamount = len(difference)
	if newamount:
		with open('previous/RSS/' + title, 'w') as pfile:
			pfile.write(data)
		return (1, difference, newamount)
	return (0, 'None')


main()
