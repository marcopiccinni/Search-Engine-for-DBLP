from Support.TextFormat import cprint
from itertools import product
from Parser.parser import publication


def find_query(string):
    words = [x for x in string.split(' ')]  # split single words
    c = True
    while c:
        c = False
        for w in words:
            if w.count('"') != 2 and w.endswith('"'):
                words[words.index(w) - 1] += ' ' + words[words.index(w)]
                words.remove(words[words.index(w)])
                c = True
    return words


def to_whoosh_query(q_list):
    ven_list = []
    pub_list = []
    for q in q_list:
        # is_venue()
        if is_publication(q, pub_list):
            continue
        elif is_venue(q, ven_list):
            continue
        pub_list.append(q)
        ven_list.append(q)

    print('[p] ', pub_list)
    print('[v] ', ven_list)
    return ' OR '.join(pub_list), ' OR '.join(ven_list)
    # return pub_list, ven_list, all_list


def is_publication(string, list):
    s = ''
    if string.startswith(
            tuple([str(x[0] + x[1]) for x in product(publication + ['inproc', 'publication', ], (':', '.'))])):
        if string.count('.'):
            s += string[string.index('.') + 1:]
            if not s.startswith(('author:', 'title:', 'year:'), ):
                return False
            if not string.startswith('publication'):
                s += ' pubtype:' + string[:string.index('.')]
        else:
            s += string[string.index(':') + 1:]
            if not string.startswith('publication'):
                s += ' pubtype:' + string[:string.index(':')]
                if not s.startswith(('author:', 'title:', 'year:'), ):
                    return False

        list.append('(' + s + ')')
        return True
    return False


def is_venue(string, list):
    if string.startswith(('venue.', 'venue:'), ):
        if string[5] == ':':
            list.append('(' + string[6:] + ')')
        elif string.startswith(('title:', 'publisher:'), 6):
            list.append('(' + string[string.index('.') + 1:] + ')')
        return True
    return False

if __name__ == '__main__':
    string = 'article.author:"Marco Piccinni" venue.title:"Questo è un test" publication:"Computer science" ' \
             'venue:prova "Sembra davvero funzionare" sembra'
    words = find_query(string)
    # print(words)
    print(to_whoosh_query(words))
