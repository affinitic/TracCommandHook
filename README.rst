TracCommandHook
===============

``TracCommandHook`` is a Trac plugin that executes a specified command after
ticket creation or modification. The command is called only if the ticket
is created with (or changed to) a specified priority.

The command and its options must be specified in trac.ini : ::

    [commandhook]
    command = /usr/local/bin/growlnotify
    priorities = blocker
    param.title-fields = summary
    param.title-parameter = -t
    param.message-fields = priority,summary
    param.message-parameter = -m


More doc to come :-)
