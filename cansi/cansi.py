import curses


def mkcolor():
    """
    Start pairs at 100 so we're less likely to clobber user defined pairs.
    """
    color = {}

    for i in range(1, 8):
        curses.init_pair(i + 100, i, -1)  # color fg on black bg
        curses.init_pair(i + 107, curses.COLOR_WHITE, i)  # white fg on color bg
        curses.init_pair(i + 114, curses.COLOR_BLACK, i)  # black fg on color bg
        color[str(i + 30)] = curses.color_pair(i + 100)
        color[str(i + 40)] = curses.color_pair(i + 107)
        color["0;" + str(i + 30)] = curses.color_pair(i + 100)
        color["0;" + str(i + 40)] = curses.color_pair(i + 107)
        color[str(i + 30) + ";0"] = curses.color_pair(i + 100)
        color[str(i + 40) + ";0"] = curses.color_pair(i + 107)
        color[str(i + 90)] = curses.color_pair(i + 100) | curses.A_BOLD
        color["1;" + str(i + 30)] = curses.color_pair(i + 100) | curses.A_BOLD
        color["1;" + str(i + 40)] = curses.color_pair(i + 107) | curses.A_BOLD
        color[str(i + 30) + ";1"] = curses.color_pair(i + 100) | curses.A_BOLD
        color[str(i + 40) + ";1"] = curses.color_pair(i + 107) | curses.A_BOLD

    return color


# pylint: disable=too-few-public-methods
class Cansi:
    """
    Curses Ansi Parser
    """

    def __init__(self, window):
        assert curses.has_colors(), "Curses wasn't configured to support colors."
        curses.use_default_colors()  # https://stackoverflow.com/a/44015131

        self.window = window
        self.color = mkcolor()
        self.attr = {
            "1": curses.A_BOLD,
            "4": curses.A_UNDERLINE,
            "5": curses.A_BLINK,
            "7": curses.A_REVERSE,
        }

    # pylint: disable=invalid-name
    def addstr(self, y, x, string):
        """
        Adds the color-formatted string to the given window, in the given
        coordinates

        ANSI escapes (CSI - Control Sequence Introducers) always start with
        \\e, \033 (octal), \x1b (hex) or \001b. They’re just various ways of
        inserting byte 27 into a string. In an ASCII table, 0x1b is called ESC,
        and this is why.
        """
        ansi_split = string.split("\x1b[")
        color_pair = curses.color_pair(0)

        # Print the first part of the string without color change
        self.window.addstr(y, x, ansi_split[0], color_pair)
        x += len(ansi_split[0])

        # Iterate over the rest of the string-parts and print them with their colors
        for substring in ansi_split[1:]:
            if substring.startswith("0K"):
                return  # 0K = clrtoeol so we are done with this line

            if substring.startswith("1G"):
                x = 0
            else:
                ansi_code = substring.split("m")[0]
                substring = substring[len(ansi_code) + 1 :]
                if ansi_code in ["1", "4", "5", "7", "8"]:
                    color_pair = color_pair | self.attr[ansi_code]
                elif ansi_code not in ["0", "0;"]:
                    color_pair = self.color[ansi_code]

            if substring:
                self.window.addstr(y, x, substring, color_pair)
                x += len(substring)
