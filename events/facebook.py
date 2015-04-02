import urllib.request
import json

previous = []

def download(url):
	request = urllib.request.urlopen(url)
	data = request.read()
	try:
		decoded = data.decode('utf-8')
	except UnicodeDecodeError:
		return 1
	return decoded

def facebook(url):
	'''facebook
	Checks if you have any new facebook notifications
	params:
		- url - The url of your facebook notification feed, NEEDS TO BE JSON SYNTAX.
	
	Please note, this gets a list when run the first time, so it will not blast you with a list of notifications when you run onEVENT. It only gets new notifications after you run it.
	'''
	global previous

	try:
		current_feed = download(url)
	except:
		print('Error grabbing facebook feed.')
		return (0, 'None')
	
	feed_object = json.loads(current_feed)
	notifications = feed_object['entries']

	difference = []
	if previous == []:
		previous = notifications

	for x in notifications:
		if not any(x['id'] == p['id'] for p in previous):
			difference.append(x)

	previous = notifications
	if len(difference):
		return (1, len(difference), difference[0]['title'])
	return(0, 'None')


if __name__ == '__main__':
	help(facebook)
