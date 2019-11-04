from Support.TextArt import welcome_text, menu_text
from GUI.menu import Menu

if __name__ == "__main__":
    welcome_text('green', 'blink')
    menu_text('orange', 'bold')
    menu = Menu()
    menu.start()
