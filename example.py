#!/usr/bin/env python

import curses
from cansi import Cansi


def event_loop(stdscr):
    curses.curs_set(0)  # hide the cursor
    cansi = Cansi(stdscr)
    lines = [
        "\u001b[1;32m\rThis line is bright GREEN\r\u001b[0m",
        "\x1b[1;31mThis line is bright RED\x1b[0m",
        "\033[0;32mThis line is GREEN\033[0m",
        "\033[0;31mThis line is RED\033[0m",
        "\x1b[0;44mThis line has a BLUE background\x1b[0m",
        "\x1b[41;1mThis line has a bright RED background\x1b[0m",
        "\033[1mThis line is \033[1;33mBOLD\033[0m",
        "\033[4mThis line is \033[1;35m\033[4mUNDERLINED\033[0m",
        "\033[5mThis line \033[1;36m\033[5mBLINKS\033[0m",
        "\033[7mThis line is \033[1mREVERSE\033[0m",
        "\033[0KTHIS LINE WON'T BE DISPLAYED\033[0m",
        "\033[1;37m\nPress q to quit\033[0m",
    ]
    while True:
        for index, line in enumerate(lines):
            cansi.addstr(index, 0, line)
        if stdscr.getkey() == "q":
            break


curses.wrapper(event_loop)
