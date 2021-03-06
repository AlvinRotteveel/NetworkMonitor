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
from agent.server import Server
from client.client import Client


sniffer = SocketCapture()
server = Server(('0.0.0.0', 1234))


def view(stdscr):
    global connection
    connection = None
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
    centered(stdscr, 31, "[4] Run agent/server                      ")
    centered(stdscr, 32, "[5] Bunny!                                ")
    centered(stdscr, 34, "[ESC] Quit                                ")
    stdscr.refresh()

    return act_on_input(stdscr, {ESC: quit,
                                 "1": live,
                                 "2": history,
                                 "3": client,
                                 "4": agent,
                                 "5": bunny})


def live(stdscr):
    stdscr.clear()

    if not sniffer.isAlive() and not connection:
        stdscr.clear()
        draw_menu(stdscr, "Live Network Traffic")
        centered(stdscr, HEIGHT // 2,
                 "Sniffing agent is not running, start the agent first, or connect to agent. Home (ESC)")
        stdscr.refresh()
        return act_on_input(stdscr, {ESC: home})
    elif connection:
        draw_columns(stdscr)
        response = connection.send('live')
        draw_packets(stdscr, 22, 'live', True, response)
        draw_menu(stdscr, "Live Network Traffic")
        while True:
            ev = stdscr.getch()
            if ev == ESC:
                stdscr.nodelay(False)
                return home(stdscr)
            # Not the neatest way.....
            else:
                time.sleep(0.1)
                stdscr.clear()
                response = connection.send('live')
                draw_packets(stdscr, 22, 'live', True, response)
                draw_menu(stdscr, "Live Network Traffic")
    else:
        draw_columns(stdscr)
        draw_packets(stdscr, 22, 'live', False)
        draw_menu(stdscr, "Live Network Traffic")
        while True:
            ev = stdscr.getch()
            if ev == ESC:
                stdscr.nodelay(False)
                return home(stdscr)
            # Not the neatest way.....
            else:
                time.sleep(0.1)
                stdscr.clear()
                draw_packets(stdscr, 22, 'live', False)
                draw_menu(stdscr, "Live Network Traffic")


def history(stdscr):
    stdscr.clear()
    draw_menu(stdscr, "Network Traffic History")

    if not sniffer.isAlive():
        stdscr.clear()
        draw_menu(stdscr, "Network Traffic History")
        centered(stdscr, HEIGHT // 2,
                 "Sniffing agent is not running, start the agent first, or connect to agent. Home (ESC)")
        stdscr.refresh()
        return act_on_input(stdscr, {ESC: home})


def client(stdscr, input=""):
    global server_ip
    prev_input = ""
    redraw = None
    selected_result = None

    stdscr.clear()
    draw_menu(stdscr, "Connect to agent")
    if connection:
        connected(stdscr)
        stdscr.refresh()
    else:
        centered(stdscr, HEIGHT // 2, "Fill in the IP of the agent/server:")
        addstr(stdscr, HEIGHT // 2 + 2, WIDTH // 2 - 8, "_" * 15, curses.A_DIM)
        addstr(stdscr, HEIGHT // 2 + 2, WIDTH // 2 - 8, input[:15])
        curses.curs_set(2)
        stdscr.refresh()

        stdscr.nodelay(True)

        while True:
            if input != prev_input or (redraw and (redraw is True or redraw.is_set())):
                if input != prev_input:
                    prev_input = input
                else:
                    redraw = None

                stdscr.clear()
                draw_menu(stdscr, "Connect to agent")
                centered(stdscr, HEIGHT // 2, "Fill in the IP of the agent/server:")

                addstr(stdscr, HEIGHT // 2 + 2, WIDTH // 2 - 8, "_" * 15, curses.A_DIM)
                server_ip = input
                addstr(stdscr, HEIGHT // 2 + 2, WIDTH // 2 - 8, server_ip[:15])

                stdscr.refresh()

            ev = stdscr.getch()
            if ev == SP:
                selected_result = None
                input += " "
            elif ev == curses.KEY_RESIZE:
                set_dimensions(stdscr)
            elif ev in (BS, DEL, curses.KEY_BACKSPACE):
                if selected_result:
                    redraw = True
                    selected_result = None
                else:
                    input = input[:-1]
            # On ESC go back to home menu
            elif ev == ESC:
                stdscr.nodelay(False)
                curses.curs_set(0)
                return home(stdscr)
            # On Enter connect to server socket with given IP
            elif ev == ord("\n"):
                stdscr.nodelay(False)
                curses.curs_set(0)
                connect(stdscr, server_ip)
            elif isalnum(ev) or ev in (ord(","), ord("."), ord("-")):
                selected_result = None
                input += chr(ev)

            time.sleep(0.01)


def connect(stdscr, server_ip):
    global connection
    connection = Client()
    connection.connect(server_ip)
    return connected(stdscr)


def connected(stdscr):
    stdscr.clear()
    draw_menu(stdscr, "Connect to agent")
    addstr(stdscr, HEIGHT // 2, (WIDTH // 2) - 20, "Client connection active to: " + server_ip)
    addstr(stdscr, HEIGHT // 2 + 2, (WIDTH // 2) - 31, "Go back to the home menu (ESC) to gather data,"
                                                       " (D) to disconnect")
    stdscr.refresh()

    ev = stdscr.getch()
    if ev == ESC:
            stdscr.nodelay(False)
            curses.curs_set(0)
            return home(stdscr)


def agent(stdscr):
    stdscr.clear()
    stdscr.border()

    if sniffer.isAlive():
        running = 2
        centered(stdscr, 29, "Agent and server running")
        stdscr.refresh()
    else:
        running = 5
        centered(stdscr, 29, "Agent and server stopped")
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
    centered(stdscr, 34, "Press (S) to start the agent/server, or (K) to kill it, home (ESC)")
    stdscr.refresh()

    while True:
            ev = stdscr.getch()
            if ev == ord("s"):
                sniffer.__init__()
                sniffer.start()
                server.serve_forever()
                agent(stdscr)
            elif ev == ord("k"):
                sniffer.cancel()
                centered(stdscr, 29, "      Quiting....      ")
                stdscr.refresh()
                time.sleep(1)
                agent(stdscr)
            elif ev == ESC:
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
    centered(stdscr, 26, "               (ESC) home                  ")

    stdscr.refresh()

    while True:
            ev = stdscr.getch()
            if ev == ord("q"):
                return quit
            elif ev == curses.KEY_RESIZE:
                set_dimensions(stdscr)
            elif ev == ESC:
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
    addstr(stdscr, 21, 5, '=' * (WIDTH - 10))
    addstr(stdscr, 20, 5, "Packet#")
    addstr(stdscr, 20, 15, "Type")
    addstr(stdscr, 20, 22, "From")
    addstr(stdscr, 20, 42, "To")
    addstr(stdscr, 20, 62, "Version")
    addstr(stdscr, 20, 72, "S. Port")
    addstr(stdscr, 20, 82, "D. Port")
    addstr(stdscr, 20, 92, "TTL")


def draw_packets(stdscr, *args):
    lineh = args[0]
    mode = args[1]
    remote = args[2]

    if not remote:
        data = get_last_packet('13')
    elif remote:
        data = args[3]

    draw_columns(stdscr)


    stdscr.nodelay(True)

    try:
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
    except:
        pass


def draw_menu(stdscr, s):
    line = '=' * (WIDTH - 10)
    addstr(stdscr, 2, 5, "(ESC) Home")
    addstr(stdscr, 2, WIDTH - len(s) - 5, s, curses.color_pair(2))
    centered(stdscr, 3, line)
    if connection:
        addstr(stdscr, 2, WIDTH // 2 - 7, "Remote data")
    else:
        addstr(stdscr, 2, WIDTH // 2 - 7, "Local data")
    stdscr.border()


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


def addinput(stdscr, y, x, s):
    curses.echo()
    stdscr.addstr(y, x, s)
    stdscr.refresh()
    input = stdscr.getstr(y + 1, x, 20)
    addstr(stdscr, (HEIGHT // 2), (WIDTH // 2) - 17, "_" * 34, curses.A_DIM)
    addstr(stdscr, (HEIGHT // 2), (WIDTH // 2) - 17, input[:34])
    return input


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
