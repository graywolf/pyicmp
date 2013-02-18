pyicmp
======

Python 3 library implementing ICMP protocol and some usefull
applications of it (at the moment ping and traceroute).

It is definitely possible to use it in paralel (multiprocessing)
and maybe possible to use it in multithreading (based on random numbers).
As long as each instance of Handler is running with different
process id, you are safe.

Requirements
============

This library requires root permissions (administrator on windows).

Traceroute
----------

This library uses Echo Request variant of traceroute, UDP variant is not
implemented, it's one of possible extensions for the future.

Examples
========

See traceroute.py and ping.py for usage example, pretty straightforward.

In a nutshell - you can use handler.handle_packet() to send messages defined
in messages.* .

Ping
----

I suggest you should read docstring for ping.Ping() and see example at
the bottom of the file (ping.py).

Traceroute 
----------

I suggest you should read docstring for traceroute.TraceRoute() and see example at
the bottom of the file (traceroute.py).
