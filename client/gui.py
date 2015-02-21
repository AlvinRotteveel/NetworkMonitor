import curses
import itertools
from curses.ascii import (isalnum,
                          BS,
                          DEL,
                          ESC,
                          SP,
                          TAB)

def View(stdscr):
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
    centered(stdscr, 26, "(q/ESC) quit")
    stdscr.refresh()

    return act_on_input(stdscr, {"q": confirm_quit,
                                 ESC: quit})

def set_dimensions(screen):
    global WIDTH
    global HEIGHT

    HEIGHT, WIDTH = screen.getmaxyx()

def draw_logo(stdscr):
    x = (WIDTH - 100) // 2
    addstr(stdscr, 2, x, "                                                            @@@.                                   ")
    addstr(stdscr, 3, x, "                                                           @@@@@                                   ")
    addstr(stdscr, 4, x, " %%%,                                                    #@@@@#                                    ")
    addstr(stdscr, 5, x, " @@@*                                                   @@@@@                                      ")
    addstr(stdscr, 6, x, " @@@*                                                  %@@@@                                       ")
    addstr(stdscr, 7, x, " @@@*                                           ...    @@.                                         ")
    addstr(stdscr, 8, x, " @@@*                 .@@@@@@@@@@/         /@@@@@@@@@@@@      @@@ /@@@@@@@@%     (@@@          @@@ ")
    addstr(stdscr, 9, x, " @@@*               (@@@@@,   .@@@@&     #@@@@%    (@@@@@     @@@@@@,    &@@@@    @@@#        &@@, ")
    addstr(stdscr, 10, x, " @@@*              @@@@@         @@@@   @@@@(         @@@@,   @@@@         &@@@    @@@.      ,@@%  ")
    addstr(stdscr, 11, x, " @@@*             %@@@@           @@@& *@@@%          ,@@@@   @@@           @@@,    @@@      @@@   ")
    addstr(stdscr, 12, x, " @@@*             @@@@@           &@@@ &@@@.           @@@@   @@@           %@@%    .@@&    @@@    ")
    addstr(stdscr, 13, x, " @@@*             @@@@@           @@@@ #@@@*           @@@@   @@@           &@@#     (@@*  /@@.    ")
    addstr(stdscr, 14, x, " @@@*             .@@@@,         .@@@,  @@@@          &@@@(   @@@#          @@@       &@@  @@(     ")
    addstr(stdscr, 15, x, " @@@*               @@@@&       %@@@,    @@@@,       @@@@,    @@@@@       ,@@@,        @@@@@@      ")
    addstr(stdscr, 16, x, " @@@@@@@@@@@@@@@@@   @@@@@@@@@@@@@%        @@@@@@@@@@@@/      @@@.@@@@@@@@@@@           @@@@       ")
    addstr(stdscr, 17, x, "                  ,@@@  .%@@@@&,              .(%%#,          @@@    *#%/.              @@@        ")
    addstr(stdscr, 18, x, "                &@@@@                                         @@@                      (@@*        ")
    addstr(stdscr, 19, x, "               @@@@@                                          @@@                  . .@@@#         ")
    addstr(stdscr, 20, x, "             @@@@@#                                           @@@                  @@@@@           ")
    addstr(stdscr, 21, x, "           ,@@@@@                                                                                  ")
    addstr(stdscr, 22, x, "             &@/                                                                                   ")


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
            for k,v in actions.iteritems():
                if ev in key(k):
                    if isinstance(v, list):
                        return v[0](*v[1:])
                    return v(screen)

def confirm_quit(screen):
    screen.clear()
    screen.border()
    draw_logo(screen)
    centered(screen, 20, "QUITING LOOPY")
    centered(screen, 24, "Quit? (y/n)")
    screen.refresh()

    return act_on_input(screen, {"y": quit, "n": home})