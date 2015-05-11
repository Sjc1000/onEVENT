# onEVENT

onEVENT is an event based automation tool for Linux. It watches events such as battery percentage, input devices, cpu and even facebook notifications. You can specify any Terminal command to be run when these event results are what you want them to be.

## Command line arguments

This program supports a few command line params. None of these are needed to run the program.

- --verbose -v		: Verbose mode. Tells the program to output information to the terminal. It uses my pprint lib which makes things look purrdy :3
- --folder		: The folder the event files are located in. Defaults to events/
- --file		: The JSON file that your events are in. Defaults to events.json
- --timeout		: The delay between checking all the events. Defaults to 1.
- --server -s		: Makes onEVENT send data through sockets.
- --host -o		: The hostname to bind on. Defaults to ''
- --port -p		: The port to bind on. Defaults to 9987
- --local -l		: Makes it run on local mode. Not default.

## Event file

onEVENT uses a 3rd party library for YAML parsing. If you don't have this, it uses my old parser.

When you have PyYAML

```YAML
- onEVENT:
    repeat: 0
    delay:
        seconds: 1
    when:
        - procexists:
            params: 
                - banshee
            result: True
    do:
        - action:
            - notify-send
            - Banshee open
            - Lowering your volume so you don't get blasted with sound!
        - action:
            - amixer
            - set
            - Master
            - 60%
    alternative:
        - action:
            - notify-send
            - Banshee closed
            - Raising volume back to 100%
        - action:
            - amixer
            - set
            - Master
            - 100%
```

**Here is how it works**

- repeat - Specify 1 if you want this to repeat over and over, even if the state doesn't go from True to false or False to True.
- delay - The delay between running of events. Can be a combonation of seconds minutes or hours.
- when - Events to run
- params - The params for the event.
- result - What you want the event to be. True / False / 1 / 0
- do - The actions
- action - The linux command to run. Each param is seperated by newline or like [param1, param2, param2]. You can specify more than one of these.

( optional )

- alternative - The alternative actions to run.
- action - The linux command to run when the event switches to false. You can specify more than one of these.


When you don't have PyYAML

```YAML
battery(full) = 1:
    repeat: 0
    delay: {'seconds': 0}
    action: [['notify-send', 'Battery', 'Battery is fully charged.']]
``` 

**Here is how it works**

event(params) = result:
    repeat: 0
    delay: {'seconds': 0}
    action: [['some', 'action']]

- event is the event name.
- params is a comma seperated list of params
- result is what state you want the event to be in to do the action.

- repeat - Specify 1 if you want this to repeat over and over, even if the state doesn't go from True to false or False to True.
- delay - The delay in between the event's run.
- action - The action to do when all events meet their result. 

( optional )

- alternative - The action to do when one of the events don't meet their result.


Each action should be seperated like the following:

[['actioncommand', 'param1', 'param2'], ['another_action', '-t', 'param for -t']]    

### Combining events

You can combine events. It's really simple.

```YAML
event1(params) = 1 & event2(params) = 0:
```

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

Please pay attention to what file the error is coming from then search for the linux file it may be. For example, if the battery event puts out an error google 'linux ( your distro ) battery class file' or something similar. 

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

When you have the YAML library.

```YAML
- onEVENT:
    repeat: 0
    delay:
        seconds: 1
    when:
        - newfile:
            params:
                - /media/steven/
            result: True
    do:
        - action:
            - notify-send
            - New mount
            - A new directory has been mounted "{0}"
```

When you don't have the YAML library.

Notifies me when my battery is charging.

```YAML
battery(charging) = 1:
    repeat: 0
    delay: {'seconds': 0}
    action: [['notify-send', 'Battery', 'Battery is charging ({0}%)']]
    alternative: [['notify-send', 'Battery', 'Battery is discharging. ({0}%)']]
```

Notifies me when my battery is full.

```YAML
battery(full) = 1:
    repeat: 0
    delay: {'seconds': 0}
    action: [['notify-send', 'Battery', 'Battery is fully charged.']]
```

Notifies me when i plug / unplug my hard drive.

```YAML
exists(/media/steven/External) = 1:
    repeat: 0
    delay: {'seconds': 0}
    action: [['notify-send', 'External HD', 'External HD has been plugged in.']]
    alternative: [['notify-send', 'External HD', 'External HD has been un-plugged.']]
```

## Server

onEVENT has the ability to send data over sockets. It sends event info in json format.

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
