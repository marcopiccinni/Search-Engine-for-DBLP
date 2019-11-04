from Indexer.ix_functions import check_ixs
from Support.TextFormat import cprint, form
from Query.make_query import MakeQuery


class Menu:
    __result_limit = 10
    __ranking = 'frequency'  # 'default'  #
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

            self.last_selected = input(form('Type your choice:\n>\t'))
            if self.last_selected == '1':
                if self.__ranking == 'frequency':
                    MakeQuery.frequency(MakeQuery(), self.__result_limit)
                else:
                    MakeQuery.vettoriale(MakeQuery(), self.__result_limit)
                # stampa
            elif self.last_selected == '2':
                pass
            elif self.last_selected == '3':
                pass
            elif self.last_selected == '4':
                return
            else:
                cprint('Ritenta, sarai più fortunato.', 'orange', 'bold', 'url', start='\t', end='\n\n')
