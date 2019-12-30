from Indexer.ix_functions import check_ixs
from Support.TextFormat import cprint, form
from Ranking.Methods import Rank


class Menu:
    """The Menu class"""

    __result_limit = 10
    __ranking = 'bm25f'
    __fuzzy = False
    __last_selected = 0
    __output_level = 2
    __choices_list = [('1. ', 'Make a search.'),
                      ('2. ', 'Change settings.'),
                      ('3. ', 'Print active settings.'),
                      ('4. ', 'Exit.'),
                      ]
    __options_list = [('1. ', 'Ranking.'),
                      ('2. ', 'Limits.'),
                      ('3. ', 'Fuzzyterm.'),
                      ('4. ', 'Output level.'),
                      ('5. ', 'Reset settings.'),
                      ]
    __ranking_list = [('1. ', 'bm25f model.'),
                      ('2. ', 'Frequency model.'),
                      ]
    __level_list = [('1. ', 'Essential output.'),
                    ('2. ', 'Default output.'),
                    ('3. ', 'Complete output.'),
                    ]

    __colornumber = ('lightgreen', 'bold',)
    __colortext = ('lightgreen',)
    __colorinput = ('purple', 'bold',)

    def start(self):
        """a function that starts the menu loop"""
        check_ixs()
        while True:
            cprint('MAIN MENU\n', 'green', 'bold', 'url', start='\n\t')
            for choice in self.__choices_list:
                print(form(choice[0], *self.__colornumber), form(choice[1], *self.__colortext))
            self.__last_selected = input(form('\nType your choice:\n>  ', *self.__colorinput))

            # ----------- Search ---------------------1
            if self.__last_selected == '1':
                rank = Rank(self.__result_limit, self.__output_level)
                if self.__ranking == 'frequency':
                    rank.frequency(self.__fuzzy)
                else:
                    rank.bm25f(self.__fuzzy)

            # ------------ Settings ---------------------
            elif self.__last_selected == '2':
                for option in self.__options_list:
                    print(form(option[0], *self.__colornumber), form(option[1], *self.__colortext))
                c = input(form('\nWhich options do you want to edit?\n>  ', *self.__colorinput))
                if c == '1':
                    for rank in self.__ranking_list:
                        print(form(rank[0], *self.__colornumber), form(rank[1], *self.__colortext))
                    c = input(form('\nWhich options do you want to choose?\n>  ', *self.__colorinput))
                    if c == '2':
                        self.__ranking = 'frequency'
                    else:
                        self.__ranking = 'bm25f'
                elif c == '2':
                    limit = input(form('\nHow many results do you want to print?\n>  ', *self.__colorinput))
                    self.__result_limit = int(limit)
                elif c == '3':
                    print('Fuzzyterm: ', self.__fuzzy)
                    c = input(form('\nDo you want to change it? [y/n]\n>  ', *self.__colorinput))
                    if c == 'y':
                        self.__fuzzy = not self.__fuzzy
                elif c == '4':
                    for level in self.__level_list:
                        print(form(level[0], *self.__colornumber), form(level[1], *self.__colortext))
                    c = input(form('\nWhich options do you want to choose?\n>  ', *self.__colorinput))
                    if c in [x[0].replace('. ', '') for x in self.__level_list]:
                        self.__output_level = int(c)
                elif c == '5':
                    self.reset()

            # ------- Print Settings ----------------------
            elif self.__last_selected == '3':
                o_color_key = ('pink', 'bold',)
                o_color_value = ('pink', 'italic',)
                cprint('Options: ', *o_color_key, start='\n')
                print('\t{}{}'.format(form('Ranking: ', *o_color_key),
                                      form(self.__ranking, *o_color_value)))
                print('\t{}{}'.format(form('Results limit: ', *o_color_key),
                                      form(self.__result_limit, *o_color_value)))
                print('\t{}{}'.format(form('Fuzzy: ', *o_color_key),
                                      form(self.__fuzzy, *o_color_value)))
                print('\t{}{}'.format(form('Output level: ', *o_color_key),
                                      form(self.__output_level, *o_color_value)))
                print()
            # --------- Exit -------------------------
            elif self.__last_selected == '4':
                return

            else:
                cprint('Try again, you will be luckier!', 'orange', 'bold', 'url', start='\t', end='\n\n')

    def reset(self):
        """reset options"""

        self.__result_limit = 10
        self.__ranking = 'bm25f'
        self.__fuzzy = False
        self.__output_level = 2
