import curses
import itertools
from curses.ascii import (isalnum,
                          BS,
                          DEL,
                          ESC,
                          SP,
                          TAB)
from agent.capture import SocketCapture
import time
from agent.database import get_last_packet


sniffer = SocketCapture()


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
    stdscr.nodelay(True)

    if not sniffer.isAlive():
        stdscr.clear()
        stdscr.border()
        centered(stdscr, HEIGHT // 2, "Sniffing agent is not running, start the agent first, or connect to agent. Home (H)")
        stdscr.refresh()
        return act_on_input(stdscr, {ESC: quit,
                                     "h": home})
    else:
        lineh = 22
        draw_columns(stdscr)
        data = get_last_packet('13')

        for l in data:
            addstr(stdscr, lineh, 5, str(l[0]))
            addstr(stdscr, lineh, 15, str(l[1]).upper())
            addstr(stdscr, lineh, 22, str(l[2]))
            addstr(stdscr, lineh, 42, str(l[3]))
            addstr(stdscr, lineh, 62, str(l[4]).upper())
            addstr(stdscr, lineh, 72, str(l[5]))
            addstr(stdscr, lineh, 82, str(l[6]))
            addstr(stdscr, lineh, 92, str(l[7]))
            lineh += 1
            stdscr.refresh()

        while True:
            ev = stdscr.getch()
            if ev == ord("h"):
                break
            # Not the neatest way.....
            else:
                time.sleep(1)
                stdscr.clear()
                live(stdscr)


def history(stdscr):
    stdscr.clear()
    stdscr.border()
    line = '=' * (WIDTH - 10)
    addstr(stdscr, 2, 5, "(H) Home    (ESC) Quit")
    addstr(stdscr, 2, WIDTH - 28, "Network Traffic History", curses.color_pair(2))
    centered(stdscr, 3, line)

    if not sniffer.isAlive():
        stdscr.clear()
        stdscr.border()
        centered(stdscr, HEIGHT // 2, "Sniffing agent is not running, start the agent first, or connect to agent. Home (H)")
        stdscr.refresh()
        return act_on_input(stdscr, {ESC: quit,
                                     "h": home})

def connect(stdscr, input=""):
    stdscr.clear()
    stdscr.border()
    line = '=' * (WIDTH - 10)
    addstr(stdscr, 2, 5, "(H) Home    (ESC) Quit")
    addstr(stdscr, 2, WIDTH - 21, "Connect to Agent", curses.color_pair(2))
    centered(stdscr, 3, line)

    centered(stdscr, (HEIGHT // 2) - 2, "Enter the IP address of the agent:")
    addstr(stdscr, (HEIGHT // 2), (WIDTH // 2) - 17, "_" * 34, curses.A_DIM)
    addstr(stdscr, (HEIGHT // 2), (WIDTH // 2) - 17, input[:34])
    curses.curs_set(2)

    stdscr.refresh()
    stdscr.nodelay(True)

    while True:
        time.sleep(1)

def agent(stdscr):
    stdscr.clear()
    stdscr.border()

    if sniffer.isAlive():
        running = 2
        centered(stdscr, 29, "Agent is running")
        stdscr.refresh()
    else:
        running = 5
        centered(stdscr, 29, "Agent has stopped")
        stdscr.refresh()

    centered(stdscr, 3, "Current status of the network capture agent")
    centered(stdscr, 10, "                       ,@,                        ", curses.color_pair(running))
    centered(stdscr, 11, "                      @@@@#                      ", curses.color_pair(running))
    centered(stdscr, 12, "              /@@,    @@@@&    /@@.              ", curses.color_pair(running))
    centered(stdscr, 13, "            /@@@@(    @@@@&    &@@@@.            ", curses.color_pair(running))
    centered(stdscr, 14, "           &@@@#      @@@@&      &@@@#           ", curses.color_pair(running))
    centered(stdscr, 15, "          &@@@.       @@@@&       /@@@#          ", curses.color_pair(running))
    centered(stdscr, 16, "         (@@@.        @@@@&        /@@@,         ", curses.color_pair(running))
    centered(stdscr, 17, "         @@@&         @@@@&         @@@%         ", curses.color_pair(running))
    centered(stdscr, 18, "         @@@#         #@@@,         @@@&         ", curses.color_pair(running))
    centered(stdscr, 19, "         @@@&                       @@@#         ", curses.color_pair(running))
    centered(stdscr, 20, "         /@@@,                     #@@@.         ", curses.color_pair(running))
    centered(stdscr, 21, "          %@@@*                   #@@@/          ", curses.color_pair(running))
    centered(stdscr, 22, "           %@@@&                .@@@@/           ", curses.color_pair(running))
    centered(stdscr, 23, "            .@@@@@/           #@@@@@             ", curses.color_pair(running))
    centered(stdscr, 24, "              .@@@@@@@@@@@@@@@@@@&               ", curses.color_pair(running))
    centered(stdscr, 25, "                 .#@@@@@@@@@@@/                  ", curses.color_pair(running))
    centered(stdscr, 34, "Press (S) to start the agent, or (K) to kill it, home (H)")
    stdscr.refresh()

    while True:
            ev = stdscr.getch()
            if ev == ord("s"):
                sniffer.__init__()
                sniffer.start()
                agent(stdscr)
            elif ev == ord("k"):
                sniffer.cancel()
                centered(stdscr, 29, "      Quiting....      ")
                stdscr.refresh()
                time.sleep(1)
                agent(stdscr)
            elif ev == ord("h"):
                return home(stdscr)
            elif ev == curses.KEY_RESIZE:
                set_dimensions(stdscr)


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


def draw_columns(stdscr):
    line = '=' * (WIDTH - 10)
    addstr(stdscr, 2, 5, "(H) Home    (ESC) Quit")
    addstr(stdscr, 2, WIDTH - 25, "Live Network Traffic", curses.color_pair(2))
    centered(stdscr, 3, line)
    centered(stdscr, 21, line)

    addstr(stdscr, 20, 5, "Packet#")
    addstr(stdscr, 20, 15, "Type")
    addstr(stdscr, 20, 22, "From")
    addstr(stdscr, 20, 42, "To")
    addstr(stdscr, 20, 62, "Version")
    addstr(stdscr, 20, 72, "S. Port")
    addstr(stdscr, 20, 82, "D. Port")
    addstr(stdscr, 20, 92, "TTL")

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
