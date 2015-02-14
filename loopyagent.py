#!/usr/bin/python
from agent import capture


if __name__ == "__main__":
    dump = capture.TCPDump()
    dump.start()