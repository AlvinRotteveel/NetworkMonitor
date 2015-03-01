import subprocess
import sys
import os


tcpdpath = '/usr/sbin/'  # Location of TCPDump, should be the same for Linux/Mac OS X
dumppath = sys.path[0] + '/agent/dump/capture.pcap'  # Path to temp capture file
dumpsize = 100  # Size in MB to go back in time


def start():
    """Start the execution of TCPDump"""
    subprocess.Popen(['/usr/sbin/tcpdump -s65535 -G 100 -C 100 -W 1 -w' + dumppath],
                                shell=True, preexec_fn=os.setsid, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def stop():
    """Stop the execution of TCPDump"""
    # Needs a different way of quiting the subprocess
    subprocess.Popen(['pkill tcpdump'],
                                shell=True, preexec_fn=os.setsid, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
