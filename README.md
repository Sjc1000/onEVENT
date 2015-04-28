# onEVENT

onEVENT is an event based automation tool for Linux. It watches events such as battery percentage, input devices, cpu and even facebook notifications. You can specify any Terminal command to be run when these event results are what you want them to be.

## Command line arguments

This program supports a few command line params. None of these are needed to run the program.

- --verbose | -v : Verbose mode. Tells the program to output information to the terminal. It uses my pprint lib which makes things look purrdy :3
- --folder	 : The folder the event files are located in. Defaults to events/
- --file	 : The JSON file that your events are in. Defaults to events.json
- --timeout	 : The delay between checking all the events. Defaults to 1.

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
- [X]	Brightness
- [X]	CPU Percentage
- [ ]	Email
- [X]	Facebook Notification ( Outdated. Use the RSS event now :) )
- [X]	File changed
- [X]	Filepath Exists
- [X]	Input Device plugged in
- [X]	Internet connection
- [X]	Lid closed ( Laptop )
- [X]	New file in directory
- [X]	Process exists
- [X]	Power button press
- [X]	RAM Usage
- [X]	RSS
- [ ]	Temperature
- [X]	Time
- [X]	Uptime
- [ ]	Many more!


**notes**

Some of these commands load from files that may be different on your system. If you experience an error like 'FileNotFound' or something similar you may need to change some code. If you're not familiar with Python this may not be easy. 

Please pay attention to what file the error is coming from then search for the linux file it may be. For example, if the battery event puts out an error like this google 'linux ( your distro ) battery class file' or something similar. 

You will then need to change the directory in the event file. This should be easy to locate, since only 1 part of my code should look like a file directory.


####Battery
The battery percentage may not be the same as your monitor one is. This does not mean its wrong, i have no idea how the system monitors it.

I might be doing the math wrong, but i've checked multiple sources and they all they thats how you do it.

####Facebook Notification
Yes, you heard right! This program supports Facebook Notifications. This runs through the RSS event now. So make sure to use that one!

1. Open your facebook to https://www.facebook.com/notifications
2. Click the little RSS button. This is next to the 'Get Notifications via Text message'.
4. Paste the link into your event param, the next param can be anything, just make it different since it uses this as the name of the file that stores the previous RSS info. So something like 'Facebook_Feed'.

####RAM

The ram does not find the 'usable' amount. It just goes off the max amount your PC has. This means it might be different that either your system monitor, or other programs such as conky.


## Adding your own events

Say what? I can add my own events?!?
Yes, you certainly can. It is very easy.

Just make a new .py file in the events folder, name it whatever you want.
Inside the file define a function that is the same as your file name. For example if i want, say a weather event. Ill name it weather.py and put in

```Python
def weather(params):
	#code
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

If the first item is 1 the event returns true, 0 is false. You can also return params, which can be used in the 'action' in the events file.

For example, if i return (1, 'This is a test!')
and in the action i use {0}, {0} will get replaced with This is a test!
{0} is the first param you return, {1} is the second, and so on.
You can specify more params and use {1}, {2}, {3}  to your desire!
Fun huh? :D

## Examples

Here are a few quick examples of events you could set up.

**Notify you when your battery is full**
```JSON
{"on": [{"event": "battery", "params": ["full"], "result": "1"}],
	"action": [["notify-send", "Battery", "Battery is now fully charged!"]],
	"repeat": "0",
	"delay": {"seconds": "5"}
}
```

**Lower system volume when the program Banshee ( music player ) is open. Volume back to 100% when Banshee is closed.**
This is useful if you forget to turn down your volume and you get blasted with loud noise.
```JSON
{"on": [{"event": "procexists", "params": ["banshee"], "result": "1"}],
	"action": [["amixer", "sset", "'Master'", "60%"]],
	"repeat": "0",
	"delay": {"seconds": "1"},
	"alternative": [["amixer", "sset", "'Master'", "100%"]]
}
```

**If the time is past 10pm and you close your lid. Shut the PC down.**
```JSON
{"on": [{"event": "lidclosed", "params": [], "result": "1"},
		{"event": "time", "params": ["later", "%H", "22"], "result": "1"}],
	"action": [["shutdown", "-h", "now"]],
	"repeat": "0",
	"delay": {"seconds": "1"}
}
```

**This has to be run with sudo python3 onEVENT.py**

## Notes

You should be aware that some of these events might not return the same results as your system. For example, on my system, my program measures the battery level at roughly 2% different than my system does. I have no idea what my system is doing, or if my math is wrong ( multiple sources say it's right ). This should not discourage you from using this program, though, you should be aware of this little glitch. 

If you are able to make a better equation that has better results i would be very glad to see it and possibly implement it into these events.


### Root commands

If the command you have defined in "action" requires root to run, by default it will fail. You can run sudo python3 onEVENT.py to give onEVENT the ability to run root commands.


## Contact

If you wish to contact me you can use any of these methods:

- Email
	- Main 		> 42Echo6Alpha@gmail.com
	- Alternative 	> Sjc1000@hotmail.com or insertfunnyaddress@hotmail.com

- IRC
	I am on IRC quite often.
	server:	irc.freenode.net ( port 6667 by default )
	channel: #Sjc_Bot is my channel, If im Sjc_AFK i am not connected. I have a bouncer that changes to AFK when i disconnect.


## Thanks

Thank you for using my software. This is and always will be free to use. I will not charge a dime for any of my solo development projects.
