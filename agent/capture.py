import subprocess
import sys
import os
import signal


class TCPDump():
    """Capture specific interface and save to PCAP."""
    def __init__(self):
        self.tcpdpath = '/usr/sbin/'
        self.dumppath = sys.path[0] + '/agent/dump/capture'

    def start(self):
        """Start the execution of TCPDump"""
        while True:
            self.process = subprocess.Popen(['/usr/sbin/tcpdump'],
                                        shell=True, preexec_fn=os.setsid)
            self.process.wait()

    def stop(self):
        """Stop the execution of TCPDump"""
        os.killpg(self.process.pid, signal.SIGTERM)

    def getdumps(self, *args):
        """Get the paths or amount of paths"""
        if args == 'amount':
            return os.listdir(self.dumppath)