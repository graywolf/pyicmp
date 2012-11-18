pyicmp
======

Python 3 library implementing ICMP protocol and some usefull
applications of it (traceroute, ...).

## traceroute

This library uses Echo Request variant of traceroute, UDP variant is not
implemented, it's one of possible extensions for the future.

Requirements
============

This library requires root permissions (administrator on windows).

Examples
========

See traceroute.py and ping.py for usage example, pretty straightforward.

In a nutshell - you can use handler.handle_packet() to send messages defined
in messages.* .

## Ping

I suggest you should read docstring for ping.Ping() and see example at
the bottom of the file (ping.py).

## Traceroute 

I suggest you should read docstring for traceroute.TraceRoute() and see example at
the bottom of the file (traceroute.py).
