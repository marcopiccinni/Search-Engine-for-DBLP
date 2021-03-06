from Support.TextFormat import cprint


def welcome_text(*args, start='', end='\n'):
    cprint(
        """
        ██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗
        ██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝
        ██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗  
        ██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝  
        ╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗
         ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝
        """, *args, start='', end='\n')


def menu_text(*args, start='', end='\n'):
    cprint(
        """
   ___  ___  __   ___    ____                 __     ____          _         
  / _ \/ _ )/ /  / _ \  / __/__ ___ _________/ /    / __/__  ___ _(_)__  ___ 
 / // / _  / /__/ ___/ _\ \/ -_) _ `/ __/ __/ _ \  / _// _ \/ _ `/ / _ \/ -_)
/____/____/____/_/    /___/\__/\_,_/_/  \__/_//_/ /___/_//_/\_, /_/_//_/\__/ 
                                                           /___/             
 """, *args, start='', end='\n')
