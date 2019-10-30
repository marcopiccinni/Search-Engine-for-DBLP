def threshold_rank(publications, venues):
    doc_limit = min(len(publications), len(venues))
    threshold = 0
    output = []
    couple = False
    set_results = set()
    for i in range(doc_limit):
        threshold = publications[i].score + venues[i].score

        elem = None
        couple = False
        # ciclo per pub
        for venue in venues:
            if publications[i].crossref == venue.key:
                couple = True
                elem = {
                    'score': publications[i].score + venue.score,
                    'pub':
                        {'title': publications[i]['title'],
                         'authors': publications[i]['author'].split('\n'),
                         'ee': publications[i]['ee'],
                         'url': publications[i]['url'],
                         'year': publications[i]['year'],
                         'journal': publications[i]['journal'],
                         'volume': publications[i]['volume'],
                         'number': publications[i]['number'],
                         'pages': publications[i]['pages'],
                         },
                    'ven':
                        {'title': venue['title'],
                         'publisher': venue['publisher'],
                         'author': venue['author'].split('\n'),
                         'year': venue['year'],
                         'journal': venue['journal'],
                         'url': venue['url'],
                         'ee': venue['ee'],
                         }
                }
                break
        if not couple:
            elem = {
                'score': publications[i].score,
                'pub':
                    {'title': publications[i]['title'],
                     'authors': publications[i]['author'].split('\n'),
                     'ee': publications[i]['ee'],
                     'url': publications[i]['url'],
                     'year': publications[i]['year'],
                     'journal': publications[i]['journal'],
                     'volume': publications[i]['volume'],
                     'number': publications[i]['number'],
                     'pages': publications[i]['pages'],
                     },
                'ven': None,
            }
        set_results.add(elem)

        elem = None
        couple = False
        # ciclo per ven
        for publication in publications:
            if publication.crossref == venues[i].key:
                couple = True
                elem = {
                    'score': publication.score + venues[i].score,
                    'pub':
                        {'title': publication['title'],
                         'authors': publication['author'].split('\n'),
                         'ee': publication['ee'],
                         'url': publication['url'],
                         'year': publication['year'],
                         'journal': publication['journal'],
                         'volume': publication['volume'],
                         'number': publication['number'],
                         'pages': publication['pages'],
                         },
                    'ven':
                        {'title': venues[i]['title'],
                         'publisher': venues[i]['publisher'],
                         'author': venues[i]['author'].split('\n'),
                         'year': venues[i]['year'],
                         'journal': venues[i]['journal'],
                         'url': venues[i]['url'],
                         'ee': venues[i]['ee'],
                         }
                }
                break
        if not couple:
            elem = {
                'score': venues[i].score,
                'pub': None,
                'ven':
                    {'title': venues[i]['title'],
                     'publisher': venues[i]['publisher'],
                     'author': venues[i]['author'].split('\n'),
                     'year': venues[i]['year'],
                     'journal': venues[i]['journal'],
                     'url': venues[i]['url'],
                     'ee': venues[i]['ee'],
                     }
            }
        set_results.add(elem)

        # using sorted and lambda to print list sorted by score.
        # the max score is check with current threshold.
        if sorted(list(set_results), key=lambda s: s['score'], reverse=True)[0]['score'] > threshold:
            return sorted(list(set_results), key=lambda s: s['score'], reverse=True)
