from Query.uquery import to_whoosh_query
from Query.print_query import q_print
from whoosh.qparser import MultifieldParser, QueryParser, SimpleParser
from Indexer.ix_functions import check_ixs
from Support.TextFormat import cprint
from Ranking.Threshold import threshold_rank as tr
from Support.TextFormat import cprint, form

from whoosh.scoring import Frequency


class MakeQuery:

    @staticmethod
    def __ask_query():
        return input(form('What do you want to search?\n>\t'))

    @staticmethod
    def __results(plist, vlist, limit):
        plist = sorted(plist, key=lambda s: s['score'], reverse=True)
        vlist = sorted(vlist, key=lambda s: s['score'], reverse=True)

        count = 0
        for element in tr(plist, vlist):
            if count == limit:
                return
            q_print(element, count + 1)
            count += 1

    def vettoriale(self, result_limit):
        pquery, vquery = to_whoosh_query(self.__ask_query())
        pix, vix = check_ixs(silent=True)

        # ----------- PUBLICATIONS ----------------------
        with pix.searcher() as ps:
            # "" search for phrase in which the maximum distance between each word is 1
            # '' if you have to include characters in a term that are normally threated specially by the parsers, such
            #   as spaces, colons, or brackets.
            pquery = MultifieldParser(['pubtype', 'author', 'title', 'year'], pix.schema).parse(pquery)
            # termclass=FuzzyTerm)

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

    def frequency(self, result_limit):
        pquery, vquery = to_whoosh_query(self.__ask_query())
        print(pquery)
        pquery = pquery.split(' OR ')
        vquery=vquery.split(' OR ')
        print(pquery)
        pix, vix = check_ixs(silent=True)

        # ----------- PUBLICATIONS ----------------------
        with pix.searcher(weighting=Frequency) as ps:
            # "" search for phrase in which the maximum distance between each word is 1
            # '' if you have to include characters in a term that are normally threated specially by the parsers, such
            #   as spaces, colons, or brackets.
            presults = None
            for pq in pquery:
                pquery = QueryParser('title', pix.schema).parse(pq)
                print(pq)
                if presults is not None:
                    tresult = ps.search(pquery, limit=5, )
                    presults.upgrade_and_extend(tresult)
                else:
                    presults = ps.search(pquery, limit=5, )

            cprint('Publications found: ' + str(len(presults)), 'bold', 'lightgrey', 'url', start='\n\t', end='\n\n')
            plist = []
            for el in presults:
                tmp = {'key': '', 'score': el.score, 'pub': dict(), 'ven': '', 'selected': 0, }
                for attr in el.items():
                    tmp['pub'][attr[0]] = attr[1]
                plist.append(tmp)

        # --------------- VENUES --------------------------
        with vix.searcher() as vs:
            vquery = MultifieldParser(['title', 'publisher'], vix.schema).parse(vquery)
            vresults = vs.search(vquery, limit=None)

            cprint('Venues found: ' + str(len(vresults)), 'bold', 'lightgrey', 'url', start='\t', end='\n')
            vlist = []
            for el in vresults:
                tmp = {'key': '', 'score': el.score, 'ven': dict(), 'pub': '', 'selected': 0, }
                for attr in el.items():
                    tmp['ven'][attr[0]] = attr[1]
                vlist.append(tmp)

            self.__results(plist, list(), limit=result_limit)
