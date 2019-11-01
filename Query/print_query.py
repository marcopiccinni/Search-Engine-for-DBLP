from Support.TextFormat import cprint, form


def q_print(element, count):
    # cprint(element['pub'], 'red')
    cprint(str(count) + ')')
    cprint(str(element['score']))
    if not element['pub'] == '':
        cprint(element['pub']['title'])
        authors = element['pub']['author'].split('\n')
        cprint(', '.join(authors[:len(authors) - 1]))
        cprint(element['pub']['year'])

    if not element['ven'] == '':
        cprint('venue: ', 'yellow')
        cprint(element['ven']['title'],end='')
        cprint(element['ven']['publisher'], end='')

    print()
