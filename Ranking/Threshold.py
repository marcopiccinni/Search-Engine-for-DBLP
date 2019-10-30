def _p_element(pub, ven_list):
    elem = dict()
    elem['pub'] = {'title': pub['title'],
                   'authors': pub['author'].split('\n'),
                   'ee': pub['ee'],
                   'url': pub['url'],
                   'year': pub['year'],
                   'journal': pub['journal'],
                   'volume': pub['volume'],
                   'number': pub['number'],
                   'pages': pub['pages'],
                   }
    couple = False
    for venue in ven_list:
        if pub.crossref == venue.key:
            couple = True
            elem['score'] = pub.score + venue.score
            elem['venue'] = {'title': venue['title'],
                             'publisher': venue['publisher'],
                             'author': venue['author'].split('\n'),
                             'year': venue['year'],
                             'journal': venue['journal'],
                             'url': venue['url'],
                             'ee': venue['ee'],
                             }
            break
    if not couple:
        elem['score'] = pub.score
        elem['ven'] = None,
    return elem


def _v_element(ven, pub_list):
    elem = dict()
    elem['ven'] = {'title': ven['title'],
                   'publisher': ven['publisher'],
                   'author': ven['author'].split('\n'),
                   'year': ven['year'],
                   'journal': ven['journal'],
                   'url': ven['url'],
                   'ee': ven['ee'],
                   }
    couple = False
    for publication in pub_list:
        if publication.crossref == ven.key:
            couple = True
            elem['score'] = publication.score + ven.score,
            elem['pub'] = {'title': publication['title'],
                           'authors': publication['author'].split('\n'),
                           'ee': publication['ee'],
                           'url': publication['url'],
                           'year': publication['year'],
                           'journal': publication['journal'],
                           'volume': publication['volume'],
                           'number': publication['number'],
                           'pages': publication['pages'],
                           },
        break
    if not couple:
        elem['score'] = ven.score,
        elem['pub'] = None


def threshold_rank(publications, venues):
    doc_limit = min(len(publications), len(venues))
    set_results = set()

    for i in range(doc_limit):
        threshold = publications[i].score + venues[i].score

        set_results.add(_p_element(publications[i], venues))
        set_results.add(_v_element(venues[i], publications))
        # using sorted and lambda to print list sorted by score.
        # the max score is check with current threshold.
        ordered_list = sorted(list(set_results), key=lambda s: s['score'], reverse=True)
        if ordered_list[0]['score'] > threshold:
            return ordered_list
    return False
