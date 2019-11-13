from Support.TextFormat import cprint, form


def q_print(element, count, level):
    """ This function provide the documents output to the user."""

    title = ('bold', 'lightgrey')
    argument = ('italic', 'lightgrey')

    bash_space = '\n' + '\t'*3 + ' ' *2

    cprint(str(count) + ')\t' + 'score: ' + str(round(element['score'], 5)), 'lightcyan', end='')

    # ----------------- Publication ----------------
    if not element['pub'] == '':
        cprint('Publication', 'yellow', 'bold', start='\n')
        # pubtype   level 2
        if level >= 2:
            print('\t{}{}'.format(form('Type: ', *title),
                                    form(element['pub']['pubtype'], *argument)))
        # title     level 1
        if element['pub']['title'] != '':
            print('\t{}{}'.format(form('Title: ', *title),
                                    form(element['pub']['title'], *argument)),
                  end='')
            if element['pub']['title'].endswith('\n') is False:
                print()
        # author    level 1
        if element['pub']['author'] != '':
            authors = element['pub']['author'].split('\n')
            print('\t{}{}'.format(form('Author: ', *title),
                                    form(', '.join(authors[:len(authors) - 1]), *argument)))
        # year      level 2
        if element['pub']['year'] != '' and level >= 2:
            print('\t{}{}'.format(form('Year: ', *title),
                                    form(element['pub']['year'], *argument)),
                  end='')
        # journal   level 2
        if element['pub']['journal'] != '' and level >= 2:
            print('\t{}{}'.format(form('Journal: ', *title),
                                    form(element['pub']['journal'], *argument)),
                  end='')
        # volume    level 3
        if element['pub']['volume'] != '' and level >= 3:
            print('\t{}{}'.format(form('Volume: ', *title),
                                    form(element['pub']['volume'], *argument)),
                  end='')
        # number    level 3
        if element['pub']['number'] != '' and level >= 3:
            print('\t{}{}'.format(form('Number: ', *title),
                                    form(element['pub']['number'], *argument)),
                  end='')
        # pages     level 3
        if element['pub']['pages'] != '' and level >= 3:
            print('\t{}{}'.format(form('Pages: ', *title),
                                    form(element['pub']['pages'], *argument)),
                  end='')
        # url       level 1
        if element['pub']['url'] != '':
            print('\t{}{}'.format(form('Link: ', *title),
                                    form('https://dblp.uni-trier.de/' + element['pub']['url'], *argument)),
                  end='')
        # ee        level 1
        if element['pub']['ee'] != '':
            ee = element['pub']['ee'].split('\n')
            print('\t{}{}'.format(form('Alternative link: ', *title),
                                    form(bash_space.join(ee[:len(ee) - 1]), *argument)))

    # ------- Venue -----------------
    if not element['ven'] == '':
        if element['pub'] == '':
            print()
        cprint('Venue', 'yellow', 'bold', start='')

        # pubtype   level 2
        if element['ven']['pubtype'] != '' and level >= 2:
            print('\t{}{}'.format(form('Type: ', *title),
                                    form(element['ven']['pubtype'], *argument)))
        # title     level 1
        if element['ven']['title'] != '':
            print('\t{}{}'.format(form('Title: ', *title),
                                    form(element['ven']['title'].replace('\n', ''), *argument)))
            if element['ven']['title'].endswith('\n') is False:
                print()
        # publisher level 1
        if element['ven']['publisher'] != '':
            print('\t{}{}'.format(form('Publisher: ', *title),
                                    form(element['ven']['publisher'], *argument)),
                  end='')
        # author    level 3
        if element['ven']['author'] != '' and level >= 3:
            authors = element['ven']['author'].split('\n')
            print('\t{}{}'.format(form('Author: ', *title),
                                    form(', '.join(authors[:len(authors) - 1]), *argument)))
        # isbn      level 2
        if element['ven']['isbn'] != '' and level >= 2:
            isbn = element['ven']['isbn'].split('\n')
            print('\t{}{}'.format(form('ISBN: ', *title),
                                    form(', '.join(isbn[:len(isbn)-1]), *argument)))
        # journal   level 3
        if element['ven']['journal'] != '' and level >= 3:
            print('\t{}{}'.format(form('Journal: ', *title),
                                    form(element['ven']['journal'], *argument)),
                  end='')
        # year      level 3
        if element['ven']['year'] != '' and level >= 3:
            print('\t{}{}'.format(form('Year: ', *title),
                                    form(element['ven']['year'], *argument)),
                  end='')
        # url       level 2
        if element['ven']['url'] != '' and level >= 2:
            print('\t{}{}'.format(form('Link: ', *title),
                                    form('https://dblp.uni-trier.de/' + element['ven']['url'], *argument)),
                  end='')
        # ee        level 2
        if element['ven']['ee'] != '' and level >= 2:
            ee = element['ven']['ee'].split('\n')
            print('\t{}{}'.format(form('Alternative link: ', *title),
                                    form(bash_space.join(ee[:len(ee) - 1]), *argument)))

    print()
