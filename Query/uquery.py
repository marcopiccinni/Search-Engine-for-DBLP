from itertools import product
from Parser.parser import publication


def to_whoosh_query(string):
    """ Used to transform the user query in the whoosh query language.
        Return the two string for the whoosh parser (publication and venue respectly)."""

    q_list = _find_query(string)
    pub_list = []
    ven_list = []
    for q in q_list:
        if _is_publication(q, pub_list):
            continue
        elif _is_venue(q, ven_list):
            continue
        # If it isn't exactly in ones, query goes in both.
        pub_list.append('(' + q + ')')
        ven_list.append('(' + q + ')')
    return ' OR '.join(pub_list), ' OR '.join(ven_list)


def _find_query(string):
    """ Used to obtain the single user queries.
        The query user format is: -----
        """
    words = [x for x in string.split(' ')]  # Split single words by spaces.
    c = True
    while c:  # Regroup the phrases with " .
        c = False
        # If the currently word ends with ", it will be grouped with the previous one.
        # The currently words is removed to the list.
        # If there isn't changes the function ends.
        for w in words:
            if w.count('"') != 2 and w.endswith('"'):
                words[words.index(w) - 1] += ' ' + words[words.index(w)]
                words.remove(w)
                c = True
                continue
            # to regroup words that is search term but spaces separeted
            if words[words.index(w) - 1].endswith(':'):
                words[words.index(w) - 1] += words[words.index(w)]
                words.remove(w)
                c = True

    return words


def _is_publication(string, list):
    """ Return True and updates the publication_list if a query is well formatted for the publication index."""

    s = ''
    # First check if the first word is a publication type. it could ends with a . or a : .
    if string.startswith(
            tuple([str(x[0] + x[1]) for x in product(publication + ['inproc', 'publication', ], (':', '.'))])):
        # In this case an attribute is specified.
        if string.count('.'):
            s += string[string.index('.') + 1:]
            if not s.startswith(('author:', 'title:', 'year:'), ):
                # ERROR
                return True
            if not string.startswith('publication'):
                s += ' pubtype:' + string[:string.index('.')]
        else:
            s += string[string.index(':') + 1:]
            if not string.startswith('publication'):
                s += ' pubtype:' + string[:string.index(':')]
        list.append('(' + s + ')')
        return True
    return False


def _is_venue(string, list):
    """ Return True and updates the venue_list if a query is well formatted for the venue_index."""

    if string.startswith(('venue.', 'venue:'), ):
        if string[5] == ':':
            list.append('(' + string[6:] + ')')
        elif string.startswith(('title:', 'publisher:'), 6):
            list.append('(' + string[string.index('.') + 1:] + ')')
        else:
            # ERROR
            return True
        return True
    return False


if __name__ == '__main__':
    string = 'article.author: "Marco Piccinni" publication.title: "Questo è un test" article:"Computer science" ' \
             'venue:prova "Sembra davvero funzionare" sembra'
    pub_query, ven_query = to_whoosh_query(string)
    print('[p] ', pub_query)
    print('[v] ', ven_query)
