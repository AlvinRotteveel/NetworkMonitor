# Loopy - Network Monitor
Unix Networkprogramming: Network Monitori

Case

A system administrator has to administer several linux based servers which are located at several locations. He would like to monitor the network activity of these servers to detect any suspicious traffic as soon as possible.

At two different locations he has a desk with a linux computer. However, he is often "working in the field" and is of course, not always at his desk, or work location. It should be possible to monitor the network traffic at multiple locations simultaniously on linux based clients.

Analysis

The goal is to build a framework to intercept and monitor network traffic.

Preconditions:

Must run on Linux
Must be written in Python
Must have minimum negative impact on connection conditions
Must have simple user interface -> npyscreen
Must have text based user interface -> npyscreen
Must show real time data
Must show historic data
Must have modular / extendible user interface
Must show information about IP
Must show information about TCP
Must show information about DNS
Must have modular / extendible protocol analysis
Must support multiple simultaneous monitoring agents (ie. multiple systems)
Must support multiple simultaneous user interface connections on the same system
Must support multiple simultaneous user interface connections on multiple systems
Research questions:

What is the most efficient way to tap network connections using Python?
What can be found about the IP protocol in the network data?
What can be found about the TCP protocol in the network data?
What can be found about the DNS protocol in the network data?
What connection types are available in Python?
What is the most efficient way to analyse and distribute network data?
How to build a versatile text based user interface using Python?
…
…
Design

Research questions:

Who are the stakeholders?
What are their concerns?
What options are there to deal with the concerns?
What are the design decisions?
Make the views that show all design decisions.

################
# Dependencies #
################

npyscreen
socket
