import curses
import itertools
from curses.ascii import (isalnum,
                          BS,
                          DEL,
                          ESC,
                          SP,
                          TAB)


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
    centered(stdscr, 30, "[3] Other...                              ")
    centered(stdscr, 32, "[ESC] Quit                                ")
    stdscr.refresh()

    return act_on_input(stdscr, {ESC: quit})


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
