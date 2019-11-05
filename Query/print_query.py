from Support.TextFormat import cprint, form


def q_print(element, count, level):
    """ This function provide the documents output to the user."""

    title = ('bold',)
    argument = ('italic',)

    cprint(str(count) + ')\t\t' + 'score: ' + str(round(element['score'], 5)), end='')

    # ----------------- Publication ----------------
    if not element['pub'] == '':
        cprint('Publication', 'yellow', 'bold', start='\n\t')
        # pubtype   level 2
        if level >= 2:
            print('\t\t{}{}'.format(form('Type: ', *title),
                                    form(element['pub']['pubtype'], *argument)))
        # title     level 1
        if element['pub']['title'] != '':
            print('\t\t{}{}'.format(form('Title: ', *title),
                                    form(element['pub']['title'], *argument)),
                  end='')
            if element['ven']['title'].endswith('\n') is False:
                print()
        # author    level 1
        if element['pub']['author'] != '':
            authors = element['pub']['author'].split('\n')
            print('\t\t{}{}'.format(form('Author: ', *title),
                                    form(', '.join(authors[:len(authors) - 1]), *argument)))
        # year      level 2
        if element['pub']['year'] != '' and level >= 2:
            print('\t\t{}{}'.format(form('Year: ', *title),
                                    form(element['pub']['year'], *argument)),
                  end='')
        # journal   level 2
        if element['pub']['journal'] != '' and level >= 2:
            print('\t\t{}{}'.format(form('Journal: ', *title),
                                    form(element['pub']['journal'], *argument)),
                  end='')
        # volume    level 3
        if element['pub']['volume'] != '' and level >= 3:
            print('\t\t{}{}'.format(form('Volume: ', *title),
                                    form(element['pub']['volume'], *argument)),
                  end='')
        # number    level 3
        if element['pub']['number'] != '' and level >= 3:
            print('\t\t{}{}'.format(form('Number: ', *title),
                                    form(element['pub']['number'], *argument)),
                  end='')
        # pages     level 3
        if element['pub']['pages'] != '' and level >= 3:
            print('\t\t{}{}'.format(form('Pages: ', *title),
                                    form(element['pub']['pages'], *argument)),
                  end='')
        # url       level 1
        if element['pub']['url'] != '':
            print('\t\t{}{}'.format(form('Link: ', *title),
                                    form('https://dblp.uni-trier.de/' + element['pub']['url'], *argument)),
                  end='')
        # ee        level 1
        if element['pub']['ee'] != '':
            ee = element['pub']['ee'].split('\n')
            print('\t\t{}{}'.format(form('Alternative link: ', *title),
                                    form('\n\t\t\t\t\t\t  '.join(ee[:len(ee) - 1])), *argument))

    # ------- Venue -----------------
    if not element['ven'] == '':
        if element['pub'] == '':
            print()
        cprint('Venue', 'yellow', 'bold', start='\t')

        # pubtype   level 2
        if element['ven']['pubtype'] != '' and level >= 2:
            print('\t\t{}{}'.format(form('Type: ', *title),
                                    form(element['ven']['pubtype'], *argument)))
        # title     level 1
        if element['ven']['title'] != '':
            print('\t\t{}{}'.format(form('Title: ', *title),
                                    form(element['ven']['title'].replace('\n', ''), *argument)))
            if element['ven']['title'].endswith('\n') is False:
                print()
        # publisher level 1
        if element['ven']['publisher'] != '':
            print('\t\t{}{}'.format(form('Publisher: ', *title),
                                    form(element['ven']['publisher'], *argument)),
                  end='')
        # author    level 3
        if element['ven']['author'] != '' and level >= 3:
            authors = element['ven']['author'].split('\n')
            print('\t\t{}{}'.format(form('Author: ', *title),
                                    form(', '.join(authors[:len(authors) - 1]), *argument)))
        # journal   level 3
        if element['ven']['journal'] != '' and level >= 3:
            print('\t\t{}{}'.format(form('Journal: ', *title),
                                    form(element['ven']['journal'], *argument)),
                  end='')
        # year      level 3
        if element['ven']['year'] != '' and level >= 3:
            print('\t\t{}{}'.format(form('Year: ', *title),
                                    form(element['ven']['year'], *argument)),
                  end='')
        # url       level 3
        if element['ven']['url'] != '' and level >= 3:
            print('\t\t{}{}'.format(form('Link: ', *title),
                                    form('https://dblp.uni-trier.de/' + element['ven']['url'], *argument)),
                  end='')
        # ee        level 3
        if element['ven']['ee'] != '' and level >= 3:
            ee = element['ven']['ee'].split('\n')
            print('\t\t{}{}'.format(form('Alternative link: ', *title),
                                    form('\n\t\t\t\t\t\t  '.join(ee[:len(ee) - 1])), *argument))

    print()
