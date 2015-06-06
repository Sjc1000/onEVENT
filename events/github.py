

import os
import socket
import urllib.request
import json


def main():
	if os.path.exists('previous/Github/') is False:
		os.makedirs('previous/Github/')
	return None


def download(url):
	try:
		request = urllib.request.urlopen(url, timeout=60)
		data = request.read()
		decoded = data.decode('utf-8')
	except (UnicodeDecodeError, socket.timeout, urllib.error.URLError):
		raise
	return decoded


def github(user, access_token):
	previous_folder = 'previous/Github/'
	try:
		data = download('https://api.github.com/users/' + user + '/events?'
		            	'access_token=' + access_token)
	except (UnicodeDecodeError, socket.timeout, urllib.error.URLError):
		raise

	if os.path.exists(previous_folder + user) is False:
		with open(previous_folder + user, 'w') as pfile:
			pfile.write(data)
		return (0, 'None')

	with open(previous_folder + user, 'r') as pfile:
		previous = json.loads(pfile.read())

	with open(previous_folder + user, 'w') as pfile:
		pfile.write(data)

	current = json.loads(data)
	difference = [x for x in current if x not in previous]

	if len(difference):
		output = []
		for item in difference:
			if item['type'] in globals():
				output.append([globals()[item['type']](item)])
		return (1, output)
	return (0, None)


def PushEvent(e):
	user = e['actor']['login']
	size = e['payload']['size']
	repo = e['repo']['name']
	url = self.shorten_url('https://github.com/' + e['repo']['name'] + '/commits/master')
	message = e['payload']['commits'][0]['message'][:25]
	return user + ' pushed ' + str(size) + ' commit[s] to ' + repo + ' "' + message + '..." - ' + url
	
def IssuesEvent(e):
	user = e['actor']['login']
	action = e['payload']['action']
	repo = e['repo']['name']
	url = self.shorten_url(e['payload']['issue']['html_url'])
	title = e['payload']['issue']['title'][:25]
	return user + ' ' + action + ' the issue at ' + repo + ' "' + title + '..." - ' + url
	
def ForkEvent(e):
	user = e['actor']['login']
	repo = e['repo']['name']
	forkee = e['payload']['forkee']['full_name']
	return user + ' forked the repo ' + repo + ' to ' + forkee
	
def IssueCommentEvent(e):
	user = e['actor']['login']
	name = e['payload']['issue']['title'][:25]
	repo = e['repo']['name']
	url = self.shorten_url(e['payload']['issue']['html_url'])
	return user + ' commented on the issue "' + name + '" at ' + repo + ' - ' + url
	
def WatchEvent(e):
	user = e['actor']['login']
	repo = e['repo']['name']
	return user + ' starred ' + repo + '.'
	
def CreateEvent(e):
	user = e['actor']['login']
	reft = e['payload']['ref_type']
	repo = e['repo']['name']
	url = self.shorten_url(e['payload']['repository']['html_url'])
	return user + ' created a ' + reft + ' at ' + repo + ' - ' + url
	
def PullRequestEvent(e):
	user = e['actor']['login']
	action = e['payload']['action']
	repo = e['repo']['name']
	url = self.shorten_url(e['payload']['pull_request']['html_url'])
	return user + ' ' + action + ' a pull request to ' + repo + ' - ' + url


main()