from Support.TextArt import welcome_text, menu_text
from Support.TextFormat import cprint, form
from Indexer.ixs_creation import Index
import whoosh.index as index
from os.path import abspath


def check_open_ixs():
    pix = index.open_dir('indexdir/PubIndex')
    vix = index.open_dir('indexdir/VenIndex')
    print('Indexes ok!')
    return pix, vix


def check_ixs():
    try:
        return check_open_ixs()
    except:
        while True:
            cprint('Indexes not found. Search Engine needs to create them.', 'orange', 'bold')
            db_path = input(form('Insert the DBLP file path', 'orange'))
            db_path = abspath(db_path)
            try:
                Index.create_ixs(Index(db_path))
            except:
                cprint('It seems there is an error with the path. Please retry', 'red', 'bold')
                continue
            try:
                return check_open_ixs()
            except:
                cprint('It seems there is an error.', 'red', 'bold')
            break


class Menu:
    __result_limit = 10
    __ranking = 'default'
    last_selected = 0

    def reset(self):
        self.__result_limit = 10
        self.__ranking = 'default'

    def __print_options(self):
        cprint('Options:', 'url')
        print(form('Output limit: '), form(self.__result_limit))
        print(form('Ranking: '), form(self.__ranking))

    def start(self):
        check_ixs()
        choices_list = [('1. ', 'Make a search.'),
                        ('2. ', 'Change settings.'),
                        ('3. ', 'Print active settings.'),
                        ('4. ', 'Exit.'),
                        ]
        while True:
            cprint('MAIN MENU\n', 'green', 'bold', 'url', start='\t')

            for choice in choices_list:
                print(form(choice[0], 'blue', 'bold'), form(choice[1], 'lightgreen'))

            self.last_selected = input(form('Type your choice: '))
