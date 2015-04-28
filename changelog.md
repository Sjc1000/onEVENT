**1.1.2**

	- Added in an error handling to onEVENT,
		if an event has an error itl return -1
		when it does onEVENT will skip the last time / last data section.
	- Added an optional iterate param for the event.json file.
	- Removed Facebook event. Now use the RSS event.
	- Changed Time event. Has more options.
	- Added more events.
	- Added GNU General Public License to onEVENT.
	- Tasks now run once straight away, then wait depending on their delay option.

**1.1.1**

	- Added more events.
	- Fixed the timing of the events.
	- Added command line options such as -v for verbose.
	- Now uses my pprint function for printing to the command line.

**1.1.0**

	- Complete rewrite of the base system. Supports multiple events better.

**1.0.0**

	- First write of the program.
