import subprocess
import sys

class TCPDump():
    """Capture specific interface and save to PCAP."""
    def __init__(self):
        self.tcpdpath = '/usr/sbin/'
        self.dumppath = sys.path[0] + '/dump/capture'

    def start(self):
        """Start the execution of TCPDump"""
        subprocess.Popen(['/usr/sbin/tcpdump ' + '-C 10 -W 10 -w ' + self.dumppath], shell=True)

    def stop(self):
        """Stop the execution of TCPDump"""


if __name__ == "__main__":
    dump = TCPDump()
    dump.start()