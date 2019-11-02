from Query.uquery import to_whoosh_query
from Query.print_query import q_print
from whoosh.qparser import MultifieldParser, QueryParser, SimpleParser
from Indexer.ix_functions import check_ixs
from Support.TextFormat import cprint
from Ranking.Threshold import threshold_rank as tr

from whoosh.scoring import Frequency


def make_query(result_limit):
    pix, vix = check_ixs()

    pquery, vquery = to_whoosh_query('Genetic')
    psquery = pquery[:]
    with pix.searcher() as ps:
        # "" search for phrase in which the maximum distance between each word is 1
        # '' if you have to include characters in a term that are normally threated specially by the parsers, such
        #   as spaces, colons, or brackets.
        pquery = MultifieldParser(['pubtype', 'author', 'title', 'year'], pix.schema).parse(pquery)
        # termclass=FuzzyTerm)

        presults = ps.search(pquery, limit=5, )
        for el in presults:
            print(el.score, el)
    print('--------------Freq')

    with pix.searcher(weighting=Frequency) as ps:
        # "" search for phrase in which the maximum distance between each word is 1
        # '' if you have to include characters in a term that are normally threated specially by the parsers, such
        #   as spaces, colons, or brackets.

        pquery = QueryParser('title', pix.schema).parse(psquery)
        print(pquery)
        presults = ps.search(pquery, limit=5, )
        for el in presults:
            print(el.score, el)
        # termclass=FuzzyTerm)

        import os
        os.abort()

        cprint('Publications found: ' + str(len(presults)), 'bold', 'lightgrey', 'url', start='\n\t', end='\n\n')
        plist = []
        for el in presults:
            tmp = {'key': '', 'score': el.score, 'pub': dict(), 'ven': '', 'selected': 0, }
            for attr in el.items():
                tmp['pub'][attr[0]] = attr[1]
            plist.append(tmp)

    with vix.searcher() as vs:
        vquery = MultifieldParser(['title', 'publisher'], vix.schema).parse(vquery)
        vresults = vs.search(vquery, limit=None)

        cprint('Venues found: ' + str(len(vresults)), 'bold', 'lightgrey', 'url', start='\t', end='\n\n')
        vlist = []
        for el in vresults:
            tmp = {'key': '', 'score': el.score, 'ven': dict(), 'pub': '', 'selected': 0, }
            for attr in el.items():
                tmp['ven'][attr[0]] = attr[1]
            vlist.append(tmp)

    count = 0
    for element in tr(plist, vlist):
        if count == result_limit:
            return
        q_print(element, count + 1)
        count += 1
