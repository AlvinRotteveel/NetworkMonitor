import os
import curses
from client import gui


if __name__ == "__main__":
    os.environ["TERM"] = "xterm"
    curses.wrapper(gui.view)