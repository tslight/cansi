import curses
import re

COLOR_PAIRS_CACHE = {}

# Translate ANSI codes into curses colors.
ANSI_TO_CURSES = {
    "[30": curses.COLOR_BLACK,
    "[31": curses.COLOR_RED,
    "[32": curses.COLOR_GREEN,
    "[33": curses.COLOR_YELLOW,
    "[34": curses.COLOR_BLUE,
    "[35": curses.COLOR_MAGENTA,
    "[36": curses.COLOR_CYAN,
    "[90": curses.COLOR_BLACK,
    "[91": curses.COLOR_RED,
    "[92": curses.COLOR_GREEN,
    "[93": curses.COLOR_YELLOW,
    "[94": curses.COLOR_BLUE,
    "[95": curses.COLOR_MAGENTA,
    "[96": curses.COLOR_CYAN,
    "[97": curses.COLOR_WHITE,
    "[0;30": curses.COLOR_BLACK,
    "[0;31": curses.COLOR_RED,
    "[0;32": curses.COLOR_GREEN,
    "[0;33": curses.COLOR_YELLOW,
    "[0;34": curses.COLOR_BLUE,
    "[0;35": curses.COLOR_MAGENTA,
    "[0;36": curses.COLOR_CYAN,
    "[0;37": curses.COLOR_WHITE,
    "[0;90": curses.COLOR_BLACK,
    "[0;91": curses.COLOR_RED,
    "[0;92": curses.COLOR_GREEN,
    "[0;93": curses.COLOR_YELLOW,
    "[0;94": curses.COLOR_BLUE,
    "[0;95": curses.COLOR_MAGENTA,
    "[0;96": curses.COLOR_CYAN,
    "[0;97": curses.COLOR_WHITE,
    "[1;30": curses.COLOR_BLACK,
    "[1;31": curses.COLOR_RED,
    "[1;32": curses.COLOR_GREEN,
    "[1;33": curses.COLOR_YELLOW,
    "[1;34": curses.COLOR_BLUE,
    "[1;35": curses.COLOR_MAGENTA,
    "[1;36": curses.COLOR_CYAN,
    "[1;37": curses.COLOR_WHITE,
    "[30;0": curses.COLOR_BLACK,
    "[31;0": curses.COLOR_RED,
    "[32;0": curses.COLOR_GREEN,
    "[33;0": curses.COLOR_YELLOW,
    "[34;0": curses.COLOR_BLUE,
    "[35;0": curses.COLOR_MAGENTA,
    "[36;0": curses.COLOR_CYAN,
    "[37;0": curses.COLOR_WHITE,
    "[30;1": curses.COLOR_BLACK,
    "[31;1": curses.COLOR_RED,
    "[32;1": curses.COLOR_GREEN,
    "[33;1": curses.COLOR_YELLOW,
    "[34;1": curses.COLOR_BLUE,
    "[35;1": curses.COLOR_MAGENTA,
    "[36;1": curses.COLOR_CYAN,
    "[37;1": curses.COLOR_WHITE,
}


def _get_color(fg, bg):
    key = (fg, bg)
    if key not in COLOR_PAIRS_CACHE:
        # Use the pairs from 101 and after, so there's less chance they'll be
        # overwritten by the user
        pair_num = len(COLOR_PAIRS_CACHE) + 101
        curses.init_pair(pair_num, fg, bg)
        COLOR_PAIRS_CACHE[key] = pair_num

    return COLOR_PAIRS_CACHE[key]


def _color_str_to_color_pair(color):
    if color in ["[0", "[1", "[0;"]:
        fg = curses.COLOR_WHITE
    else:
        fg = ANSI_TO_CURSES[color]
    color_pair = _get_color(fg, curses.COLOR_BLACK)
    return color_pair


def addstr(window, y, x, string):
    """
    Adds the color-formatted string to the given window, in the given
    coordinates

    Only use color pairs up to 100 when using this function,
    otherwise you will overwrite the pairs used by this function
    """
    assert (
        curses.has_colors()
    ), "Curses wasn't configured to support colors. Call curses.start_color()"

    # split but \033 which stands for a color change
    color_split = re.split("\x1b|\\033|\033", string, flags=re.IGNORECASE)

    # Print the first part of the string without color change
    default_color_pair = _get_color(curses.COLOR_WHITE, curses.COLOR_BLACK)
    window.addstr(y, x, color_split[0], curses.color_pair(default_color_pair))
    x += len(color_split[0])

    # Iterate over the rest of the string-parts and print them with their colors
    for substring in color_split[1:]:
        if substring.startswith("[0K"):
            window.deleteln()
            window.clrtoeol()
        else:
            color_str = substring.split("m")[0]
            substring = substring[len(color_str) + 1 :]
            color_pair = _color_str_to_color_pair(color_str)
            window.addstr(y, x, substring, curses.color_pair(color_pair))
            x += len(substring)
