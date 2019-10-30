from Support.TextFormat import cprint


def _p_element(pub, ven_list):
    pub['ven'] = None

    for venue in ven_list:
        cprint(pub['pub']['key'], 'red', start='\t')
        if pub['pub']['crossref'] == venue['ven']['key']:
            pub['score'] = pub['score'] + venue['score']
            pub['venue'] = {'title': venue['title'],
                            'publisher': venue['publisher'],
                            'author': venue['author'].split('\n'),
                            'year': venue['year'],
                            'journal': venue['journal'],
                            'url': venue['url'],
                            'ee': venue['ee'],
                            }
            break

    return pub


def _v_element(ven, pub_list):

    try:
        if ven['pub'] is not None:
            return ven
    except KeyError:
        ven['pub'] = None

    for pub in pub_list:
        if ven['ven']['crossref'] == pub['ven']['key']:
            ven['score'] = ven['score'] + pub['score']
            ven['pub'] = {'title': pub['title'],
                          'authors': pub['author'].split('\n'),
                          'ee': pub['ee'],
                          'url': pub['url'],
                          'year': pub['year'],
                          'journal': pub['journal'],
                          'volume': pub['volume'],
                          'number': pub['number'],
                          'pages': pub['pages'],
                          },
            break

    return ven


def threshold_rank(publications, venues):
    doc_limit = min(len(publications), len(venues))
    cprint(doc_limit, 'lightgrey', start='doc_limit: ')

    set_results = set()

    for i in range(doc_limit):
        threshold = publications[i]['score'] + venues[i]['score']
        cprint(threshold, 'yellow', 'bold', start='threshold: ')

        set_results.add(_p_element(publications[i], venues))
        set_results.add(_v_element(venues[i], publications))

        # using sorted and lambda to print list sorted by score.
        # the max score is check with current threshold.
        ordered_list = sorted(list(set_results), key=lambda s: s['score'], reverse=True)
        cprint(ordered_list[0]['score'], 'red', 'bold')
        if ordered_list[0]['score'] > threshold:
            cprint(len(ordered_list), 'purple', start='len_ord_list: ')
            return ordered_list
    return False
