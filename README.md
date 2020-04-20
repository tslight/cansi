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
        "\033[1;31mThis line is bright RED\033[0m",
        "\033[0;32mThis line is GREEN\033[0m",
        "\033[0;31mThis line is RED\033[0m",
        "\033[1mThis line is BOLD\033[0m",
        "\033[4mThis line is BOLD\033[0m",
        "\033[5mThis line BLINKS\033[0m",
        "\033[7mThis line is REVERSE\033[0m",
        "\033[0KmThis line won't be displayed\033[0m",
        "\033[1;37mPress q to quit\033[0m",
    ]
    while True:
        for index, line in enumerate(lines):
            cansi.addstr(index, 0, line)
        if stdscr.getkey() == "q":
            break


curses.wrapper(event_loop)
```

## REFERENCES

https://docs.python.org/3/howto/curses.html

https://docs.python.org/3/library/curses.html

https://www.perlmonks.org/bare/?node_id=215785

http://ascii-table.com/ansi-escape-sequences.php

https://notes.burke.libbey.me/ansi-escape-codes/

https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
