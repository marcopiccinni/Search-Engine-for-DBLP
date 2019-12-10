from Support.TextFormat import cprint, form

main_obj = ('yellow', 'bold',)  # pub / venue
alt_obj = ('yellow', 'italic',)  # less rilevant pub/venue (only 2 fields: title, year)
score = ('lightcyan', 'bold')
title = ('bold', 'url', 'lightgrey')
argument = ('italic', 'lightgrey')
bash_space = '\n' + '\t' * 3 + ' ' * 2
output_form = '\t' + '{}: {}'


def print_pub(pub, level):
    """print the pub(s)"""

    # if pub is dict transform it to list
    if isinstance(pub, dict):
        tmp = list()
        tmp.append(pub)
        pub = tmp

    for p in pub:
        # pubtype   level 2
        if level >= 2:
            print(output_form.format(form('Type', *title),
                                     form(p['pubtype'], *argument)))
        # title     level 1
        if p['title'] != '':
            print(output_form.format(form('Title', *title),
                                     form(p['title'], *argument)),
                  end='')
            if p['title'].endswith('\n') is False:
                print()
        # author    level 1
        if p['author'] != '':
            authors = p['author'].split('\n')
            print(output_form.format(form('Author', *title),
                                     form(', '.join(authors[:len(authors) - 1]), *argument)))
        # year      level 2
        if p['year'] != '' and level >= 2:
            print(output_form.format(form('Year', *title),
                                     form(p['year'], *argument)),
                  end='')
        # journal   level 2
        if p['journal'] != '' and level >= 2:
            print(output_form.format(form('Journal', *title),
                                     form(p['journal'], *argument)),
                  end='')
        # volume    level 3
        if p['volume'] != '' and level >= 3:
            print(output_form.format(form('Volume', *title),
                                     form(p['volume'], *argument)),
                  end='')
        # number    level 3
        if p['number'] != '' and level >= 3:
            print(output_form.format(form('Number', *title),
                                     form(p['number'], *argument)),
                  end='')
        # pages     level 3
        if p['pages'] != '' and level >= 3:
            print(output_form.format(form('Pages', *title),
                                     form(p['pages'], *argument)),
                  end='')
        # url       level 2
        if p['url'] != '' and level >= 2:
            print(output_form.format(form('Link', *title),
                                     form('https://dblp.uni-trier.de/' + p['url'].replace('\n', ''), *argument)))
        # ee        level 2
        if p['ee'] != '' and level >= 2:
            ee = p['ee'].split('\n')
            print(output_form.format(form('Alternative link', *title),
                                     form(bash_space.join(ee[:len(ee) - 1]), *argument)), end='')
            if not ee[len(ee) - 1].endswith('\n'):
                print()


def print_venue(ven, level):
    """print the venue"""

    # pubtype   level 2
    if ven['pubtype'] != '' and level >= 2:
        print(output_form.format(form('Type', *title),
                                 form(ven['pubtype'], *argument)))
    # title     level 1
    if ven['title'] != '':
        print(output_form.format(form('Title', *title),
                                 form(ven['title'].replace('\n', ''), *argument)))
    # publisher level 1
    if ven['publisher'] != '':
        print(output_form.format(form('Publisher', *title),
                                 form(ven['publisher'], *argument)),
              end='')
    # author    level 3
    if ven['author'] != '' and level >= 3:
        authors = ven['author'].split('\n')
        print(output_form.format(form('Author', *title),
                                 form(', '.join(authors[:len(authors) - 1]), *argument)))
    # isbn      level 2
    if ven['isbn'] != '' and level >= 2:
        isbn = ven['isbn'].split('\n')
        print(output_form.format(form('ISBN', *title),
                                 form(', '.join(isbn[:len(isbn) - 1]), *argument)))
    # year      level 3
    if ven['year'] != '' and level >= 3:
        print(output_form.format(form('Year', *title),
                                 form(ven['year'], *argument)), )
    # url       level 2
    if ven['url'] != '' and level >= 2:
        print(output_form.format(form('Link', *title),
                                 form('https://dblp.uni-trier.de/' + ven['url'].replace('\n', ''), *argument)), )
    # ee        level 2
    if ven['ee'] != '' and level >= 2:
        ee = ven['ee'].split('\n')
        print(output_form.format(form('Alternative link', *title),
                                 form(bash_space.join(ee[:len(ee) - 1]), *argument)))


def print_alternative(alt):
    """print the others pubs contained in a given venue"""

    cprint('Pubs Included', *alt_obj, start='\t')
    for p in alt:
        cprint(p.strip(), *argument, start='\t- ')


def print_inven(inven, level):
    """print the venue in which the pub is contained"""

    # title         level 2
    if inven['title'] != '':
        print(output_form.format(form('Title', *title),
                                 form(inven['title'].strip(), *argument)))
    # year      level 2
    if inven['year'] != '':
        print(output_form.format(form('Year', *title),
                                 form(inven['year'].strip(), *argument)))
    # url       level 3
    if inven['url'] != '' and level >= 3:
        print(output_form.format(form('Link', *title),
                                 form('https://dblp.uni-trier.de/' + inven['url'].strip(), *argument)))
    # ee        level 3
    if inven['ee'] != '' and level >= 3:
        ee = inven['ee'].split('\n')
        print(output_form.format(form('Alternative link', *title),
                                 form(bash_space.join(ee[:len(ee) - 1]), *argument)))


def q_print(element, count, level):
    """ This function provide the documents output to the user."""

    # - pub in venue --> score = pub.score
    if len(element['alternative']) == 0 and \
            (isinstance(element['pub'], dict) or (isinstance(element['pub'], list) and len(element['pub']))):
        cprint(' ' * 2 + str(count) + ')\t' + 'score: ' + str(round(element['score'], 5)), *score)
        cprint('Publication', *main_obj, start='\t')
        print_pub(element['pub'], level)

        if len(element['ven']) and level >= 2:
            if 'added' in element.keys():
                cprint('In Venue', *alt_obj, start='\n\t')
            else:
                cprint('In Relevant Venue', *alt_obj, start='\n\t')
            print_inven(element['ven'], level)

    # - venue con alternative --> score = venue.score
    elif len(element['pub']) == 0:
        cprint(' ' * 2 + str(count) + ')\t' + 'score: ' + str(round(element['score'], 5)), *score)
        # ------- Venue -----------------
        cprint('Venue', *main_obj, start='\t')
        print_venue(element['ven'], level)

        # alternative
        if len(element['alternative']) and level >= 3:
            print_alternative(element['alternative'])

    # - venue con pubs e alternative --> score = original(venue.score + pubs.score)
    else:
        s = element['ven']['o_score']
        for x in element['pub']:
            s += x['o_score']

        cprint(' ' * 2 + str(count) + ')\t' + 'score: ' + str(round(s, 5)), *score)

        cprint('Venue', *main_obj, start='\t')
        print_venue(element['ven'], level)
        print()
        cprint('Relevant Publications', *main_obj, start='\t')
        for pub in element['pub']:
            print_pub(pub, level)
            print()

        # alternative
        if len(element['alternative']) and level >= 3:
            print_alternative(element['alternative'])

    print()
