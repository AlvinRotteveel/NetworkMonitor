#!/usr/bin/python
from agent import capture
import sys


if __name__ == "__main__":
    try:
        dump = capture.TCPDump()
        dump.start()
    except KeyboardInterrupt:
        print("Quiting...")
        dump.stop()
        sys.exit()