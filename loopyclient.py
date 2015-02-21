#!/usr/bin/python
from client import home
import sys


if __name__ == "__main__":
    try:
        client = home.Client().run()
    except KeyboardInterrupt:
        print("Quiting...")
        sys.exit()