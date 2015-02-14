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
        self.process = subprocess.Popen(['/usr/sbin/tcpdump ' + '-w ' + self.dumppath + ' -C 10 -W 10'],
                                        shell=True, preexec_fn=os.setsid)

    def stop(self):
        """Stop the execution of TCPDump"""
        os.killpg(self.process.pid, signal.SIGTERM)