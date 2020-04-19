# CURSES ANSI PARSER

## INSTALLATION

`pip install cansi`

## EXAMPLE

``` python
import curses
from cansi import Cansi


def event_loop(stdscr):
    curses.curs_set(0)  # hide the cursor
    cansi = Cansi(stdscr)
    lines = [
        "\033[1;32mThis line is bright GREEN\033[0m",
        "\033[0;32mThis line is GREEN\033[0m",
        "\033[1;31mThis line is bright RED\033[0m",
        "\033[0;31mThis line is bright RED\033[0m",
        "\033[1;37mPress q to quit\033[0m",
    ]
    while True:
        for index, line in enumerate(lines):
            cansi.addstr(index, 0, line)
        if stdscr.getkey() == "q":
            break


curses.wrapper(event_loop)
```
