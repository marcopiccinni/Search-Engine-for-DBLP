#!/usr/bin/python3
from Support.TextArt import welcome_text, menu_text
from GUI.menu import Menu
from Support.utils import clear


if __name__ == "__main__":
    clear()
    welcome_text('green', 'blink')
    menu_text('orange', 'bold')
    menu = Menu()
    menu.start()
