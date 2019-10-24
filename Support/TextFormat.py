class TextCode:
    """Container for text ANSI format codes"""
    CEND = '\33[0m'  # Closing element for the re-styled text
    # Text tipe
    BOLD = '\33[1m'
    ITALIC = '\33[3m'
    URL = '\33[4m'
    BLINK = '\33[5m'
    BLINK2 = '\33[6m'
    SELECTED = '\33[7m'
    # Standard line color
    BLACK = '\33[30m'
    RED = '\33[31m'
    GREEN = '\33[32m'
    YELLOW = '\33[33m'
    BLUE = '\33[34m'
    VIOLET = '\33[35m'
    BEIGE = '\33[36m'
    WHITE = '\33[37m'
    # Secondary line color
    GREY = '\33[90m'
    RED2 = '\33[91m'
    GREEN2 = '\33[92m'
    YELLOW2 = '\33[93m'
    BLUE2 = '\33[94m'
    VIOLET2 = '\33[95m'
    BEIGE2 = '\33[96m'
    WHITE2 = '\33[97m'
    # Standard background color
    BLACKBG = '\33[40m'
    REDBG = '\33[41m'
    GREENBG = '\33[42m'
    YELLOWBG = '\33[43m'
    BLUEBG = '\33[44m'
    VIOLETBG = '\33[45m'
    BEIGEBG = '\33[46m'
    WHITEBG = '\33[47m'
    # Secondary background color
    GREYBG = '\33[100m'
    REDBG2 = '\33[101m'
    GREENBG2 = '\33[102m'
    YELLOWBG2 = '\33[103m'
    BLUEBG2 = '\33[104m'
    VIOLETBG2 = '\33[105m'
    BEIGEBG2 = '\33[106m'
    WHITEBG2 = '\33[107m'

    @staticmethod
    def codes():
        """To stamp all the possible value could be passed to color function"""
        for text_type in tuple(TextCode.__dict__.keys())[
                         3:41]:  # [3:41] is for take only the important key for the use.
            print(text_type, end=', ')
        print('\b\b')


def form(string, *args):
    """ Called to change output text style, more args can be passed at the same time.
        It's possible change colors, styles and selection mode.
        There is also some pre-configurated background style.
    """
    text = str(string)
    for arg in args:
        color_s = str(arg).upper()
        if color_s in tuple(TextCode.__dict__.keys())[3:41]:
            text = TextCode.__dict__.get(color_s) + text
    return text + TextCode.CEND


def help():
    """Help function to now how to use it"""
    if not isANSIsupported():
        print('Your sistem may not be able to use ANSI format for text. '
              'Use only if you know what you are doing, or if the next lines are shown correctly.\n')
    print(form('Usage:', 'blue', 'bold', 'selected') +
          form('\n\tfrom Support.TextFormat import form', 'yellow') +
          form("\n\tprint(form('This is a yellow text.','yellow',...))", 'yellow') +
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