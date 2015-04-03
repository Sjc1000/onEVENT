# onEVENT

onEVENT is an event based automation tool for Linux. It watches events such as battery percentage, input devices, cpu and even facebook notifications. You can specify any Terminal command to run when these event results are what you want them to be.

## Event file

Ill explain how to add things to the event file so you can have your own events!

First, ill show you an example of an event.

```JSON
{"on": [{"event": "inputdevice", "params": ["Logitech USB Receiver"], "result": "1"}],
	"action": [["notify-send", "Mouse", "{0} connected."]],
	"repeat": "0",
	"delay": {"seconds": "0"}
}
```
This is what it all means:

```JSON
{"on": [{"*event*": "**inputdevice**", "*params*": ["**Logitech USB Receiver**"], "*result*": "**1**"}],
	"*action*": **[["notify-send", "Mouse", "{0} connected."]]**,
	"*repeat*": "**0**",
	"*delay*": **{"seconds": "**0**"}**
}
```

The things with * are the params, and the ** things are values, the ** items are the one you change.

###params

**event** - Change this to the event you want to check, this is the name of the event file in the events folder. Without the .py extension

**params** - The params you wish to pass to the event file, each event file has different params so i can't cover all of them here. Use python eventfile.py to find out info about each event.

**result** - This is 1 if you want the event to be true, 0 if you want the event to be false.

**action** - The linux terminal command/s to run when the *result* matches the event outcome.

**repeat** - 1 if you want this command to repeat until the event is false, 0 if you want the command to run 1 time until the command is false.

**delay** - The delay between checks if the event is true or false. Items can be any combination of seconds, minutes, hours.	{"seconds": 10, "minutes": 4} will check an event every 4 minutes and 10 seconds.

( optional )

**alternative** - The linux terminal command to run when the event is false.
 
 
 **notes**
 
 You can add more than 1 event, they will all have to match their *result* to be true, if not it will be false.
 
 You will notice that the terminal commands are split up, ["command", "param 1", "param 2", "-b", "param for -b"]
 This is so my program knows where the params are.


## Built in events

This is a list of events i have built, and plan to build. Feel free to contact me with any ideas or suggestions for events, i will be happy to hear them and maybe even implement them!

- [X]	Battery
- [X]	CPU Percentage
- [ ]	Email
- [X]	Facebook Notification
- [X]	Filepath Exists
- [X]	Input Device plugged in
- [X]	Internet connection
- [X]	New file in directory
- [X]	Process exists
- [ ]	RAM Usage
- [ ]	Temperature
- [X]	Time
- [X]	Uptime
- [ ]	Many more!


**notes**

####Battery
The battery percentage may not be the same as your monitor one is. This does not mean its wrong, i have no idea how the system monitors it.

I might be doing the math wrong, but i've checked multiple sources and they all they thats how you do it.

####Facebook Notification
Yes, you heard right! This program supports Facebook Notifications. You will need to pass a certain URL to the facebook event for this to work. I will explain how to get this url.

1. Open your facebook to https://www.facebook.com/notifications
2. Click the little RSS button. This is next to the 'Get Notifications via' text.
3. Change the format param of the url, by default it looks like &format=rss20, change it to &format=json
4. Paste the link into your event and you're done!

## Adding your own events

Say what? I can add my own events?!?
Yes, you certainly can. It is very easy.

Just make a new .py file in the events folder, name it whatever you want.
Inside the file define a function that is the same as your file name. For example if i want, say a weather event. Ill name it weather.py and put in
```Python
def weather(params)
	# do stuff here
	return (1, 'Output')
```

Now, you may be thinking how my program knows if this event will be true or not. You have to return a tuple in each function.

```Python
return (1, 'Param1', 'param2')
```
or

```Python
return (0, 'Param1', 'Param2')
```

If the first item is 1 the event returns true, 0 is false. You can also return params, which use can use in the 'action' in the events file.

For example, if i return (1, 'This is a test!')
and in the action i use {0}, {0} will get replaced with This is a test!
{0} is the first param you return, {1} is the second, and so on.
You can specify more params and use {1}, {2}, {3}  to your desire!
Fun huh? :D
