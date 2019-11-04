from Indexer.ix_functions import check_ixs
from Support.TextFormat import cprint, form
from Ranking.Methods import Rank


class Menu:
    __result_limit = 10
    __ranking = 'vector'
    __last_selected = 0
    __fuzzy = False
    __options_list = [('1. ', 'Ranking.'), ('2. ', 'Limits.'), ('3. ', 'Fuzzyterm.')]
    __ranking_list = [('1. ', 'Vector model.'),
                      ('2. ', 'Frequency model.'), ]
    __choices_list = [('1. ', 'Make a search.'),
                      ('2. ', 'Change settings.'),
                      ('3. ', 'Print active settings.'),
                      ('4. ', 'Exit.'),
                      ]

    def reset(self):
        self.__result_limit = 10
        self.__ranking = 'vector'
        self.__fuzzy = False

    def __print_options(self):
        cprint('Options:', 'url')
        print(form('Output limit: '), form(self.__result_limit))
        print(form('Ranking: '), form(self.__ranking))

    def start(self):
        check_ixs()
        __choices_list = [('1. ', 'Make a search.'),
                          ('2. ', 'Change settings.'),
                          ('3. ', 'Print active settings.'),
                          ('4. ', 'Exit.'),
                          ]
        while True:
            cprint('MAIN MENU\n', 'green', 'bold', 'url', start='\t')

            for choice in self.__choices_list:
                print(form(choice[0], 'blue', 'bold'), form(choice[1], 'lightgreen'))

            self.__last_selected = input(form('\nType your choice:\n>\t', 'purple', 'bold'))
            if self.__last_selected == '1':
                if self.__ranking == 'frequency':
                    Rank.frequency(Rank(), self.__result_limit, self.__fuzzy)
                else:
                    Rank.vector(Rank(), self.__result_limit, self.__fuzzy)

            elif self.__last_selected == '2':
                for option in self.__options_list:
                    print(form(option[0], 'lightgreen', 'bold'), form(option[1], 'lightgreen'))
                c = input(form('\nWhich options do you want to edit?\n>\t', 'purple', 'bold'))
                if c == '1':
                    for rank in self.__ranking_list:
                        print(form(rank[0], 'lightgreen', 'bold'), form(rank[1], 'lightgreen'))
                    c = input(form('\nWhich options do you want to choose?\n>\t', 'purple', 'bold'))
                    if c == '2':
                        self.__ranking = 'frequency'
                    else:
                        self.__ranking = 'vector'
                elif c == '2':
                    limit = input(form('\nHow many results do you want to print?\n>\t', 'purple', 'bold'))
                    self.__result_limit = int(limit)
                elif c == '3':
                    print('Fuzzyterm: ', self.__fuzzy)
                    c = input(form('\nDo you want to change it? [y/n]\n>\t', 'purple', 'bold'))
                    if c == 'y':
                        if self.__fuzzy:
                            self.__fuzzy = False
                        else:
                            self.__fuzzy = True

            elif self.__last_selected == '3':
                cprint('Options: ', 'pink', start='\n')
                cprint(self.__ranking, 'pink', start=form('\tRanking: ', 'pink'))
                cprint(self.__result_limit, 'pink', start=form('\tResults limit: ', 'pink'))
                cprint(self.__fuzzy, 'pink', start=form('\tFuzzy: ', 'pink'), end='\n\n')

            elif self.__last_selected == '4':
                return

            else:
                cprint('Ritenta, sarai più fortunato.', 'orange', 'bold', 'url', start='\t', end='\n\n')
