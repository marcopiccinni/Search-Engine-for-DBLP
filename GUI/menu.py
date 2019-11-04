from Indexer.ix_functions import check_ixs
from Support.TextFormat import cprint, form
from Ranking.Methods import Rank


class Menu:
    __result_limit = 10
    __ranking = 'frequency'  #'default'  #
    last_selected = 0
    __fuzzy = True

    def reset(self):
        self.__result_limit = 10
        self.__ranking = 'default'
        self.__fuzzy = False

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

            self.last_selected = input(form('Type your choice:\n>\t'))
            if self.last_selected == '1':
                if self.__ranking == 'frequency':
                    Rank.frequency(Rank(), self.__result_limit, self.__fuzzy)
                else:
                    Rank.vector(Rank(), self.__result_limit, self.__fuzzy)
                # stampa
            elif self.last_selected == '2': 
                pass
            elif self.last_selected == '3':
                pass
            elif self.last_selected == '4':
                return
            else:
                cprint('Ritenta, sarai più fortunato.', 'orange', 'bold', 'url', start='\t', end='\n\n')
