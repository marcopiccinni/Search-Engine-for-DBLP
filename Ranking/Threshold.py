from Support.TextFormat import cprint


def _p_element(pub, ven_list):
    pub['ven'] = None
    for ven in ven_list:
        cprint(pub['pub']['key'], 'red', start='\t')
        if not pub['pub']['crossref'] == '' and (pub['pub']['crossref'].replace('\n', '') == ven['ven']['key']):
            pub['score'] = pub['score'] + ven['score']
            pub['venue'] = {'title': ven['title'],
                            'publisher': ven['publisher'],
                            'author': ven['author'].split('\n'),
                            'year': ven['year'],
                            'journal': ven['journal'],
                            'url': ven['url'],
                            'ee': ven['ee'],
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
        if not pub['pub']['crossref'] == '' and (pub['pub']['crossref'].replace('\n', '') == ven['ven']['key']):
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
