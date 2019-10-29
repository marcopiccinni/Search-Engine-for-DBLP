class TextCode:
    """Container for text ANSI format codes"""
    CEND = '\33[0m'  # Closing element for the re-styled text
    # Text tipe
    BOLD = '\33[1m'
    ITALIC = '\33[3m'
    URL = '\33[4m'
    BLINK = '\33[5m'
    SELECTED = '\33[7m'
    # Standard line color
    BLACK = '\33[30m'
    RED = '\33[31m'
    GREEN = '\33[32m'
    ORANGE = '\33[33m'
    BLUE = '\33[34m'
    PURPLE = '\33[35m'
    CYAN = '\33[36m'
    LIGHTGREY = '\33[37m'
    # Secondary line color
    DARKGREY = '\33[90m'
    LIGHTRED = '\33[91m'
    LIGHTGREEN = '\33[92m'
    YELLOW = '\33[93m'
    LIGHTBLUE = '\33[94m'
    PINK = '\33[95m'
    LIGHTCYAN = '\33[96m'

    # Standard background color
    BLACKBG = '\33[40m'
    REDBG = '\33[41m'
    GREENBG = '\33[42m'
    ORANGEBG = '\33[43m'
    BLUEBG = '\33[44m'
    PURPLEBG = '\33[45m'
    CYANBG = '\33[46m'
    LIGHTGREYBG = '\33[47m'
    # Secondary background color
    GREYBG = '\33[100m'
    REDBG2 = '\33[101m'
    GREENBG2 = '\33[102m'
    YELLOWBG = '\33[103m'
    BLUEBG2 = '\33[104m'
    VIOLETBG = '\33[105m'
    BEIGEBG = '\33[106m'
    WHITEBG = '\33[107m'

    @staticmethod
    def codes():
        """To stamp all the possible value could be passed to color function"""
        for text_type in tuple(TextCode.__dict__.keys())[3:39]:  # [3:39] is for take only the important key to use.
            print(text_type, end=', ')
        print('\b\b')


def cprint(string, *args, start='', end='\n'):
    """ Print formatted text, more args can be passed at the same time.
            It's possible change colors, styles and selection mode.
            There is also some pre-configurated background style.
        """
    print(start + form(string, *args), end=end)


def form(string, *args):
    """ Called to change output text style, more args can be passed at the same time.
        It's possible change colors, styles and selection mode.
        There is also some pre-configurated background style.
    """
    # if not isANSIsupported():
    #     return string
    text = str(string)
    for arg in args:
        color_s = str(arg).upper()
        if color_s in tuple(TextCode.__dict__.keys())[3:39]:
            text = TextCode.__dict__.get(color_s) + text
    return text + TextCode.CEND


def help():
    """Help function to now how to use it"""
    if not isANSIsupported():
        print('Your sistem may not be able to use ANSI format for text. '
              'Use only if you know what you are doing, or if the next lines are shown correctly.\n')
    print(form('Usage:', 'blue', 'bold', 'selected') +
          form('\n\tfrom Support.TextFormat import cprint', 'yellow') +
          form("\n\tcprint('This is a yellow italic text.','yellow','italic',...)", 'yellow', 'italic') +
          '\n  ' + form('or', 'red', 'bold') +
          form('\n\tfrom Support.TextFormat import form', 'yellow') +
          form("\n\tprint(form('This is a yellow bold text.','yellow','bold',...))", 'yellow', 'bold') +
          '\n' +
          form('\nFor all the possible codes: TextCode.codes()', 'green2')
          )


def isANSIsupported():
    """Return True if the current running terminal allow ANSI format of the text,
    if it doesn't or it's not sure False is return"""
    import sys, os, time, platform
    for handle in [sys.stdout]:
        if (hasattr(handle, "isatty") and handle.isatty()) or \
                ('TERM' in os.environ and os.environ['TERM'] == 'ANSI'):
            if platform.system() == 'Windows' and not ('TERM' in os.environ and os.environ['TERM'] == 'ANSI'):
                return False
            else:
                return True
        return False


if __name__ == "__main__":
    help()
