# onEVENT

An event setup for PC. Inspiration from an Android app called Tasker.

onEVENT is designed for people who are some kind of familiar with the Linux Terminal. The output commands are Terminal commands.

## Event file

Alright, now you're probably wondering how you can add events. Each event is in a seperate file in the events/ folder, you can use python eventfile.py to find out all the info about the built in events. I will try to document all of the events i make as best as i can.

You can add an event to the events.json file. Ill explain the format of this file and how to add stuff to it :)

This is how its set out, 

[
	{"on": [{"event": "eventname", "params": ["param1","param2"], "result": "1"}], 
		"action": [["linux command 2"],["linux command 2"]], 
		"repeat": "0", 
		"delay": {"seconds": "1"},
		"alternative": [["Command to run when event is false"], ["second command"]]
	}
]

If you're familiar with the JSON syntax this will some sort of sense to you.
Ill explain what these are about:
	"eventname" is the eventname.py file ( without the .py ). It runs the event with the "params".
	"result" can be 1 if you want the eventname.py to be true, or 0 if you want it to be false.
	
	You can add more than 1 event that will be called, they will all have to match their result for the action to be run. If this is confusing i can go into further detail.
	
	"action" is the list of linux commands that you wish to run. It has double [[]] for a reason, The way the commands are set out is you need to seperate the commands params like ["command", "param1", "param2", "-b", "b param"]
	and since you can run more than one command its all contained in one big list.
	
	"action": [["notify-send","External HDD","External HDD connected! {0}"],["echo", "HD connected"]]
	
	this is an example of more than 1 command.
	
	"repeat" can be "0" or "1", 0 if you only want the command to run once the event switches from false to true. If it is 1 it will repeat depending on the "delay" param.
	"repeat" the time to wait between checking if the event is true or false. 
	{"seconds": "ammount", "minutes": "ammount", "hours": "ammount"}
	
	{"seconds": 10, "minutes": 1}
	This will run the command every minute and 10 seconds.
	"alternative" is the command to run when the event switches from true to false. This obeys the repeat and delay rules as well.
