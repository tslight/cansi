import curses
import re

# pylint: disable=too-many-instance-attributes, too-few-public-methods, too-many-statements


class Cansi:
    """
    Curses Ansi Parser
    """

    def __init__(self, window):
        assert curses.has_colors(), "Curses wasn't configured to support colors."
        curses.use_default_colors()  # https://stackoverflow.com/a/44015131

        self.window = window

        for i in range(1, 8):
            curses.init_pair(i, i, -1)
            curses.init_pair(i + 7, curses.COLOR_WHITE, i)
            curses.init_pair(i + 14, curses.COLOR_BLACK, i)

        self.red_black = curses.color_pair(1)
        self.green_black = curses.color_pair(2)
        self.yellow_black = curses.color_pair(3)
        self.blue_black = curses.color_pair(4)
        self.magenta_black = curses.color_pair(5)
        self.cyan_black = curses.color_pair(6)
        self.white_black = curses.color_pair(7)
        self.white_red = curses.color_pair(8)
        self.white_green = curses.color_pair(9)
        self.white_yellow = curses.color_pair(10)
        self.white_blue = curses.color_pair(11)
        self.white_magenta = curses.color_pair(12)
        self.white_cyan = curses.color_pair(13)
        self.white_white = curses.color_pair(14)
        self.black_red = curses.color_pair(15)
        self.black_green = curses.color_pair(16)
        self.black_yellow = curses.color_pair(17)
        self.black_blue = curses.color_pair(18)
        self.black_magenta = curses.color_pair(19)
        self.black_cyan = curses.color_pair(20)
        self.black_white = curses.color_pair(21)

        self.red_black_bold = curses.color_pair(1) | curses.A_BOLD
        self.green_black_bold = curses.color_pair(2) | curses.A_BOLD
        self.yellow_black_bold = curses.color_pair(3) | curses.A_BOLD
        self.blue_black_bold = curses.color_pair(4) | curses.A_BOLD
        self.magenta_black_bold = curses.color_pair(5) | curses.A_BOLD
        self.cyan_black_bold = curses.color_pair(6) | curses.A_BOLD
        self.white_black_bold = curses.color_pair(7) | curses.A_BOLD
        self.white_red_bold = curses.color_pair(8) | curses.A_BOLD
        self.white_green_bold = curses.color_pair(9) | curses.A_BOLD
        self.white_yellow_bold = curses.color_pair(10) | curses.A_BOLD
        self.white_blue_bold = curses.color_pair(11) | curses.A_BOLD
        self.white_magenta_bold = curses.color_pair(12) | curses.A_BOLD
        self.white_cyan_bold = curses.color_pair(13) | curses.A_BOLD
        self.white_white_bold = curses.color_pair(14) | curses.A_BOLD
        self.black_red_bold = curses.color_pair(15) | curses.A_BOLD
        self.black_green_bold = curses.color_pair(16) | curses.A_BOLD
        self.black_yellow_bold = curses.color_pair(17) | curses.A_BOLD
        self.black_blue_bold = curses.color_pair(18) | curses.A_BOLD
        self.black_magenta_bold = curses.color_pair(19) | curses.A_BOLD
        self.black_cyan_bold = curses.color_pair(20) | curses.A_BOLD
        self.black_white_bold = curses.color_pair(21) | curses.A_BOLD

        self.ansi_attr = {
            "1": curses.A_BOLD,
            "4": curses.A_UNDERLINE,
            "5": curses.A_BLINK,
            "7": curses.A_REVERSE,
        }

        self.ansi_color = {
            "0": self.white_black,
            "0;": self.white_black,
            "30": self.white_black,
            "31": self.red_black,
            "32": self.green_black,
            "33": self.yellow_black,
            "34": self.blue_black,
            "35": self.magenta_black,
            "36": self.cyan_black,
            "37": self.white_black,
            "90": self.white_black_bold,
            "91": self.red_black_bold,
            "92": self.green_black_bold,
            "93": self.yellow_black_bold,
            "94": self.blue_black_bold,
            "95": self.magenta_black_bold,
            "96": self.cyan_black_bold,
            "97": self.white_black_bold,
            "0;30": self.white_black,
            "0;31": self.red_black,
            "0;32": self.green_black,
            "0;33": self.yellow_black,
            "0;34": self.blue_black,
            "0;35": self.magenta_black,
            "0;36": self.cyan_black,
            "0;37": self.white_black,
            "0;90": self.white_black_bold,
            "0;91": self.red_black_bold,
            "0;92": self.green_black_bold,
            "0;93": self.yellow_black_bold,
            "0;94": self.blue_black_bold,
            "0;95": self.magenta_black_bold,
            "0;96": self.cyan_black_bold,
            "0;97": self.white_black_bold,
            "1;30": self.white_black_bold,
            "1;31": self.red_black_bold,
            "1;32": self.green_black_bold,
            "1;33": self.yellow_black_bold,
            "1;34": self.blue_black_bold,
            "1;35": self.magenta_black_bold,
            "1;36": self.cyan_black_bold,
            "1;37": self.white_black_bold,
            "30;0": self.white_black,
            "31;0": self.red_black,
            "32;0": self.green_black,
            "33;0": self.yellow_black,
            "34;0": self.blue_black,
            "35;0": self.magenta_black,
            "36;0": self.cyan_black,
            "37;0": self.white_black,
            "30;1": self.white_black_bold,
            "31;1": self.red_black_bold,
            "32;1": self.green_black_bold,
            "33;1": self.yellow_black_bold,
            "34;1": self.blue_black_bold,
            "35;1": self.magenta_black_bold,
            "36;1": self.cyan_black_bold,
            "37;1": self.white_black_bold,
        }

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
        color_pair = self.white_black

        # Print the first part of the string without color change
        self.window.addstr(y, x, ansi_split[0], color_pair)
        x += len(ansi_split[0])

        # Iterate over the rest of the string-parts and print them with their colors
        for substring in ansi_split[1:]:
            if substring.startswith("0K"):
                substring = substring.replace("0K", "")
            elif substring.startswith("1G"):
                x = 0
            else:
                ansi_code = substring.split("m")[0]
                substring = substring[len(ansi_code) + 1 :]
                if ansi_code in ["1", "4", "5", "7", "8"]:
                    color_pair = color_pair | self.ansi_attr[ansi_code]
                else:
                    color_pair = self.ansi_color[ansi_code]

            if substring:
                self.window.addstr(y, x, substring, color_pair)
                x += len(substring)
