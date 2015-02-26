import curses
import itertools
from curses.ascii import (isalnum,
                          BS,
                          DEL,
                          ESC,
                          SP,
                          TAB)
from agent import capture


def view(stdscr):
    set_dimensions(stdscr)
    stdscr.keypad(1)
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    home(stdscr)


def home(stdscr):
    stdscr.clear()
    stdscr.border()
    draw_logo(stdscr)
    centered(stdscr, 25, "Welcome to Loopy! Network Traffic Analyzer")
    centered(stdscr, 27, "Choose an option                          ")
    centered(stdscr, 28, "[1] Live network traffic                  ")
    centered(stdscr, 29, "[2] Network traffic history               ")
    centered(stdscr, 30, "[3] Connect to agent                      ")
    centered(stdscr, 31, "[4] Run agent                             ")
    centered(stdscr, 32, "[5] Bunny!                                ")
    centered(stdscr, 34, "[ESC] Quit                                ")
    stdscr.refresh()

    return act_on_input(stdscr, {ESC: quit,
                                 "1": live,
                                 "2": history,
                                 "3": connect,
                                 "4": agent,
                                 "5": bunny})


def live(stdscr):
    stdscr.clear()
    stdscr.border()


def history(stdscr):
    stdscr.clear()
    stdscr.border()


def connect(stdscr):
    stdscr.clear()
    stdscr.border()


def agent(stdscr):
    stdscr.clear()
    stdscr.border()

    centered(stdscr, 5, "Current status of the network capture agent")
    # Some ASCII icon to show the current status.....
    centered(stdscr, 34, "Press (S) to start the agent, (K) to kill it, or go home (H)")
    stdscr.refresh()

    while True:
            ev = stdscr.getch()
            if ev == ord("s"):
                agent_status("start")
            elif ev == ord("k"):
                if not agent_status("stop"):
                    centered(stdscr, 38, "Nothing to kill here, go kill a bunny!",curses.color_pair(5))
                    stdscr.refresh()
            elif ev == ord("h"):
                return home(stdscr)
            elif ev == curses.KEY_RESIZE:
                set_dimensions(stdscr)


def agent_status(action):
    # Initiate and start the capturing agent
    dump = capture.TCPDump()
    if action == "start":
        dump.start()
    elif action == "stop":
        r = dump.stop()
        return r

def bunny(stdscr):
    stdscr.clear()
    stdscr.border()

    centered(stdscr, 6, "                          +MM0^            ")
    centered(stdscr, 7, "                           +MMMM1          ")
    centered(stdscr, 8, "                           0MMNMM+         ")
    centered(stdscr, 9, "                           +MMMNNN         ")
    centered(stdscr, 10, "              ^^++++^^      1MMM0N1++^     ")
    centered(stdscr, 11, "         +1o00000o00000oooo1+oMM000MM00o^  ")
    centered(stdscr, 12, "       10000o000000000oo000oo00MNNMMMM000+ ")
    centered(stdscr, 13, "     o000oo0o00o0000o0000000o0000MMMMN0000+")
    centered(stdscr, 14, "   +0000000000000000oo000000000000NNN0000N0")
    centered(stdscr, 15, "  +000000NMMMMMNN00000000000000NN00000000o^")
    centered(stdscr, 16, "  0000MMMMMMMMMMMMMN00000000000MMNNMo1+^^  ")
    centered(stdscr, 17, "  0000MMMMMN000000NNNo000000000NMM1+       ")
    centered(stdscr, 18, "  100000000000000000NN00ooo000001^         ")
    centered(stdscr, 19, " 1o0000o00000000000000N000000N+            ")
    centered(stdscr, 20, "NMMMM0o00000000000000000000MM0             ")
    centered(stdscr, 21, "+o0MMMoo000000000000000000NNMNo1^          ")
    centered(stdscr, 22, "      ^o000000000o000ooooo0000NM0          ")
    centered(stdscr, 24, "            Get back to work!              ")
    centered(stdscr, 26, "            (H) home (Q) quit              ")

    stdscr.refresh()

    while True:
            ev = stdscr.getch()
            if ev == ord("q"):
                return quit
            elif ev == curses.KEY_RESIZE:
                set_dimensions(stdscr)
            elif ev == ord("h"):
                return home(stdscr)


def set_dimensions(screen):
    global WIDTH
    global HEIGHT

    HEIGHT, WIDTH = screen.getmaxyx()


def draw_logo(stdscr):
    x = (WIDTH - 100) // 2
    addstr(stdscr, 2, x, "                                                            @@@.                                   ",curses.color_pair(2))
    addstr(stdscr, 3, x, "                                                           @@@@@                                   ",curses.color_pair(2))
    addstr(stdscr, 4, x, " %%%,                                                    #@@@@#                                    ",curses.color_pair(2))
    addstr(stdscr, 5, x, " @@@*                                                   @@@@@                                      ",curses.color_pair(2))
    addstr(stdscr, 6, x, " @@@*                                                  %@@@@                                       ",curses.color_pair(2))
    addstr(stdscr, 7, x, " @@@*                                           ...    @@.                                         ",curses.color_pair(2))
    addstr(stdscr, 8, x, " @@@*                 .@@@@@@@@@@/         /@@@@@@@@@@@@      @@@ /@@@@@@@@%     (@@@          @@@ ",curses.color_pair(2))
    addstr(stdscr, 9, x, " @@@*               (@@@@@,   .@@@@&     #@@@@%    (@@@@@     @@@@@@,    &@@@@    @@@#        &@@, ",curses.color_pair(2))
    addstr(stdscr, 10, x, " @@@*              @@@@@         @@@@   @@@@(         @@@@,   @@@@         &@@@    @@@.      ,@@%  ",curses.color_pair(2))
    addstr(stdscr, 11, x, " @@@*             %@@@@           @@@& *@@@%          ,@@@@   @@@           @@@,    @@@      @@@   ",curses.color_pair(2))
    addstr(stdscr, 12, x, " @@@*             @@@@@           &@@@ &@@@.           @@@@   @@@           %@@%    .@@&    @@@    ",curses.color_pair(2))
    addstr(stdscr, 13, x, " @@@*             @@@@@           @@@@ #@@@*           @@@@   @@@           &@@#     (@@*  /@@.    ",curses.color_pair(2))
    addstr(stdscr, 14, x, " @@@*             .@@@@,         .@@@,  @@@@          &@@@(   @@@#          @@@       &@@  @@(     ",curses.color_pair(2))
    addstr(stdscr, 15, x, " @@@*               @@@@&       %@@@,    @@@@,       @@@@,    @@@@@       ,@@@,        @@@@@@      ",curses.color_pair(2))
    addstr(stdscr, 16, x, " @@@@@@@@@@@@@@@@@   @@@@@@@@@@@@@%        @@@@@@@@@@@@/      @@@.@@@@@@@@@@@           @@@@       ",curses.color_pair(2))
    addstr(stdscr, 17, x, "                  ,@@@  .%@@@@&,              .(%%#,          @@@    *#%/.              @@@        ",curses.color_pair(2))
    addstr(stdscr, 18, x, "                &@@@@                                         @@@                      (@@*        ",curses.color_pair(2))
    addstr(stdscr, 19, x, "               @@@@@                                          @@@                  . .@@@#         ",curses.color_pair(2))
    addstr(stdscr, 20, x, "             @@@@@#                                           @@@                  @@@@@           ",curses.color_pair(2))
    addstr(stdscr, 21, x, "           ,@@@@@                                                                                  ",curses.color_pair(2))
    addstr(stdscr, 22, x, "             &@/                                                                                   ",curses.color_pair(2))


def addstr(win, y, x, s, *args):
    # Bounds checking
    y = max(0, y)
    x = max(0, x)
    if y >= HEIGHT:
        return
    if x >= WIDTH:
        return
    s = s[:WIDTH - x - 1]

    return win.addstr(y, x, s, *args)


def centered(win, y, message, *args):
    addstr(win, y, int((WIDTH - len(message)) // 2), message, *args)


def act_on_input(screen, actions):
    def key(k):
        if isinstance(k, str):
            return [ord(k)]
        if isinstance(k, (list, tuple)):
            return list(itertools.chain.from_iterable(key(l) for l in k))
        return [k]

    while True:
        ev = screen.getch()
        if ev == curses.KEY_RESIZE:
            set_dimensions(screen)
        elif not isinstance(actions, dict):
            return actions(screen)
        else:
            for k, v in actions.items():
                if ev in key(k):
                    if isinstance(v, list):
                        return v[0](*v[1:])
                    return v(screen)
