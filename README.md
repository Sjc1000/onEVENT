# onEVENT

An event setup for PC. Inspiration from an Android app called Tasker.

onEVENT is designed for people who are some kind of familiar with the Linux Terminal. The output commands are Terminal commands.

## Event file

Ill explain how to add things to the event file so you can have your own events!

First, ill show you an example of an event.

```JSON
{"on": [{"*event*": "**inputdevice**", "*params*": ["**Logitech USB Receiver**"], "*result*": "**1**"}],
	"*action*": **[["notify-send", "Mouse", "{0} connected."]]**,
	"*repeat*": "**0**",
	"*delay*": **{"seconds": "**0**"}**
}
```

The things with * are the params, and the **** things are values, the ** items are the one you change.

###params
*event* - Change this to the event you want to check, this is the name of the event file in the events folder. Without the .py extension

*params* - The params you wish to pass to the event file, each event file has different params so i can't cover all of them here. Use python eventfile.py to find out info about each event.

*result* - This is 1 if you want the event to be true, 0 if you want the event to be false.

*action* - The linux terminal command/s to run when the *result* matches the event outcome.

*repeat* - 1 if you want this command to repeat until the event is false, 0 if you want the command to run 1 time until the command is false.

*delay* - The delay between checks if the event is true or false. Items can be any combination of seconds, minutes, hours.	{"seconds": 10, "minutes": 4} will check an event every 4 minutes and 10 seconds.

( optional )
 *alternative* - The linux terminal command to run when the event is false.
 
 
 **notes**
 You can add more than 1 event, they will all have to match their *result* to be true, if not it will be false.
 
 You will notice that the terminal commands are split up, ["command", "param 1", "param 2", "-b", "-b param"]
 This is so my program knows where the params are.

