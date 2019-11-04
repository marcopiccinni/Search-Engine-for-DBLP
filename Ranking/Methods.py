from Query.uquery import to_whoosh_query
from Query.print_query import q_print
from whoosh.qparser import MultifieldParser, QueryParser
from Indexer.ix_functions import check_ixs
from Ranking.Threshold import threshold_rank as tr
from Support.TextFormat import cprint, form
from whoosh.query import FuzzyTerm
from whoosh.scoring import Frequency


class Rank:
    """ Class used to get the rilevant documents and print it."""
    @staticmethod
    def __ask_query():
        return input(form('What do you want to search?\n>\t'))

    @staticmethod
    def __results(plist, vlist, limit):
        plist = sorted(plist, key=lambda s: s['score'], reverse=True)
        vlist = sorted(vlist, key=lambda s: s['score'], reverse=True)

        if len(plist) == 0:
            results = vlist
        elif len(vlist) == 0:
            results = plist
        else:
            results = tr(plist, vlist)

        count = 0
        for element in results:
            if count == limit:
                return
            q_print(element, count + 1)
            count += 1

    def vector(self, result_limit, fuzzy=False):
        pquery, vquery = to_whoosh_query(self.__ask_query())
        pix, vix = check_ixs(silent=True)

        # ----------- PUBLICATIONS ----------------------
        with pix.searcher() as ps:
            # "" search for phrase in which the maximum distance between each word is 1
            # '' if you have to include characters in a term that are normally threated specially by the parsers, such
            #   as spaces, colons, or brackets.

            if fuzzy:
                pquery = MultifieldParser(['pubtype', 'author', 'title', 'year'], pix.schema, termclass=FuzzyTerm).parse(pquery)
            else:
                pquery = MultifieldParser(['pubtype', 'author', 'title', 'year'], pix.schema).parse(pquery)

            presults = ps.search(pquery, limit=5, )

            cprint('Publications found: ' + str(len(presults)), 'bold', 'lightgrey', 'url', start='\n\t', end='\n')
            plist = []
            for el in presults:
                tmp = {'key': '', 'score': el.score, 'pub': dict(), 'ven': '', 'selected': 0, }
                for attr in el.items():
                    tmp['pub'][attr[0]] = attr[1]
                plist.append(tmp)

        # --------------- VENUES --------------------------
        with vix.searcher() as vs:
            if fuzzy:
                vquery = MultifieldParser(['title', 'publisher'], vix.schema, termclass=FuzzyTerm).parse(vquery)
            else:
                vquery = MultifieldParser(['title', 'publisher'], vix.schema).parse(vquery)


            vresults = vs.search(vquery, limit=None)

            cprint('Venues found: ' + str(len(vresults)), 'bold', 'lightgrey', 'url', start='\t', end='\n')
            vlist = []
            for el in vresults:
                tmp = {'key': '', 'score': el.score, 'ven': dict(), 'pub': '', 'selected': 0, }
                for attr in el.items():
                    tmp['ven'][attr[0]] = attr[1]
                vlist.append(tmp)

        self.__results(plist, vlist, result_limit)

    def frequency(self, result_limit, fuzzy=False):
        pquery, vquery = to_whoosh_query(self.__ask_query())
        pquery = pquery.split(' OR ')
        vquery = vquery.split(' OR ')

        pix, vix = check_ixs(silent=True)

        # ----------- PUBLICATIONS ----------------------
        with pix.searcher(weighting=Frequency) as ps:
            # "" search for phrase in which the maximum distance between each word is 1
            # '' if you have to include characters in a term that are normally threated specially by the parsers, such
            #   as spaces, colons, or brackets.
            presults = None
            for pq in pquery:
                if fuzzy:
                    pq_parse = QueryParser('title', pix.schema, termclass=FuzzyTerm).parse(pq)
                else:
                    pq_parse = QueryParser('title', pix.schema).parse(pq)

                if presults is not None:
                    tresult = ps.search(pq_parse, limit=None, )
                    presults.upgrade_and_extend(tresult)
                else:
                    presults = ps.search(pq_parse, limit=None, )

                if not pq.startswith(('title', 'author', 'year'), ):
                    if fuzzy:
                        pq_parse = QueryParser('author', pix.schema, termclass=FuzzyTerm).parse(pq)
                    else:
                        pq_parse = QueryParser('author', pix.schema).parse(pq)
                    tresult = ps.search(pq_parse, limit=None, )
                    presults.upgrade_and_extend(tresult)
                    if fuzzy:
                        pq_parse = QueryParser('year', pix.schema, termclass=FuzzyTerm).parse(pq)
                    else:
                        pq_parse = QueryParser('year', pix.schema).parse(pq)
                    tresult = ps.search(pq_parse, limit=None, )
                    presults.upgrade_and_extend(tresult)

            cprint('Publications found: ' + str(len(presults)), 'bold', 'lightgrey', 'url', start='\n\t', end='\n\n')
            plist = []
            for el in presults:
                tmp = {'key': '', 'score': el.score, 'pub': dict(), 'ven': '', 'selected': 0, }
                for attr in el.items():
                    tmp['pub'][attr[0]] = attr[1]
                plist.append(tmp)

        # --------------- VENUES --------------------------
        vresults = None
        with vix.searcher(weighting=Frequency) as vs:
            print('1: ', vquery)
            for vq in vquery:
                print('2: ', vq)
                if fuzzy:
                    vq_parse = QueryParser('title', vix.schema, termclass=FuzzyTerm).parse(vq)
                else:
                    vq_parse = QueryParser('title', vix.schema).parse(vq)
                if vresults is not None:
                    tresult = vs.search(vq_parse, limit=None)
                    vresults.upgrade_and_extend(tresult)
                else:
                    vresults = vs.search(vq_parse, limit=None)

                if not vq.startswith(('title:', 'publisher'), ):
                    if fuzzy:
                        vq_parse = QueryParser('publisher', vix.schema, termclass=FuzzyTerm).parse(vq)
                    else:
                        vq_parse = QueryParser('publisher', vix.schema).parse(vq)
                    tresult = vs.search(vq_parse, limit=None)
                    vresults.upgrade_and_extend(tresult)

            cprint('Venues found: ' + str(len(vresults)), 'bold', 'lightgrey', 'url', start='\t', end='\n')
            vlist = []
            for el in vresults:
                tmp = {'key': '', 'score': el.score, 'ven': dict(), 'pub': '', 'selected': 0, }
                for attr in el.items():
                    tmp['ven'][attr[0]] = attr[1]
                vlist.append(tmp)

        self.__results(plist, vlist, limit=result_limit)

