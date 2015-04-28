import urllib.request
import os
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import socket

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

def strip(html, item):
	if 'author' in item.tag:
		if len(item):
			return item[0].text
	s = htmlStripper()
	if html == None:
		return None
	s.feed(html)
	return s.get_data()

def strbrackets(data):
	if '}' in data:
		return data[data.find('}')+1:]
	return data

def main():
	'''main
	Checks if the RSS previous folder exists and if not, creates it.
	'''
	if not os.path.exists('previous/RSS'):
		os.makedirs('previous/RSS')
	return 0

def download(url):
	try:
		request = urllib.request.urlopen(url, timeout=30)
		data = request.read()
		decoded = data.decode('utf-8')
	except (UnicodeDecodeError, socket.timeout, urllib.error.URLError):
		return 1
	return decoded

def parse(data):
	root = ET.fromstring(data)
	items = root.findall('.//item')
	if len(items) == 0:
		items = []
		for i in root:
			if 'entry' in i.tag:
				items.append(i)
	output = []
	for child in items:
		output.append({strbrackets(i.tag):strip(i.text, i) for i in child})
	return output

def rss(rss_url, title):
	'''rss
	An RSS feed event.
	params:
		- rss_url - The url of the rss feed.
		- title - The name of the RSS. This is used to name the previous file.
	output:
		- an array of new rss events. If you specify iterate 1 in the .json file the output will be looped. If not... Im not sure ;)
	'''
	data = download(rss_url)
	if data == 1:
		return (-1, 'Error')
	current = parse(data)
	if not os.path.exists('previous/RSS/' + title):
		with open('previous/RSS/' + title, 'w') as rfile:
			rfile.write(data)
		return (0, 'None')
	with open('previous/RSS/' + title, 'r') as rfile:
		previous = parse(rfile.read())
	difference = [x for x in current if x not in previous]
	if len(difference):
		with open('previous/RSS/' + title, 'w') as rfile:
			rfile.write(data)
		return (1, difference)
	return (0, 'None')


main()
