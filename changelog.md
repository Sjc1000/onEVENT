**1.3.1**

    - Now checks for PyYAML, and if it doesn't have it. Used my custom breed of YAML.

**1.3.0**

    - Changed from JSON syntax to a custom breed of YAML

**1.2.0**
    
    - Added folderchanged event. Watches all the files modify time and returns true when one has been changed.
    - Added universal error handler. If any error happens during the running of
        event it will report the error. It will also skip the last data section, but not the last time section.
        This means it will wait for the specified time until running it again.
    - Added server capability, you can now run onEVENT as a server.
    - Bugfixes

**1.1.2**

    - Added in an error handling to onEVENT,
        if an event has an error itl return -1
        when it does onEVENT will skip the last data section.
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
