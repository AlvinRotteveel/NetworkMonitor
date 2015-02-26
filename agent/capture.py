import subprocess
import sys
import os
import signal


class TCPDump():
    """Capture specific interface and save to PCAP."""
    def __init__(self):
        self.tcpdpath = '/usr/sbin/'  # Location of TCPDump, should be the same for Linux/Mac OS X
        self.dumppath = sys.path[0] + '/agent/dump/capture.pcap'  # Path to temp capture file
        self.dumpsize = 100  # Size in MB to go back in time

    def start(self):
        """Start the execution of TCPDump"""
        self.process = subprocess.Popen(['/usr/sbin/tcpdump -s65535 -G 100 -C 100 -W 1 -w' + self.dumppath],
                                    shell=True, preexec_fn=os.setsid)
        self.process.wait()

    def stop(self):
        """Stop the execution of TCPDump"""
        try:
            os.killpg(self.process.pid, signal.SIGTERM)
            return True
        except:
            return False

