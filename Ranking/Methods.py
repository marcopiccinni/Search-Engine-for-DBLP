from Query.uquery import to_whoosh_query
from Query.print_query import q_print
from whoosh.qparser import MultifieldParser, QueryParser
from Indexer.ix_functions import check_ixs
from Ranking.Threshold import threshold_rank as tr
from Support.TextFormat import cprint, form
from whoosh.query import FuzzyTerm
from whoosh.scoring import Frequency


class Rank:
    """ Class used to get the rilevant documents and print it.
        It support two different ranking methods: Vector(default choice) or Frequency.
        It is possible to choice to search for similarity in the user query (default is False)."""

    __result_limit = None
    __output_level = None
    __output = list()
    pix = None
    vix = None
    __level = None

    def __init__(self, limit, output):
        self.__result_limit = limit
        self.__output_level = output
        self.pix, self.vix = check_ixs(silent=True)

    def __find_correlations(self, results):
        """for each venue it finds the pubblications that it contains"""

        for result in results[:self.__result_limit]:

            # pub without venue
            if len(result['ven']) == 0:
                result['alternative'] = []

                with self.vix.searcher(weighting=Frequency) as vs:
                    vq_parse = QueryParser('key', self.vix.schema).parse(result['pub']['crossref'])
                    tresult = vs.search(vq_parse, limit=None, )
                    if len(tresult) != 0:
                        result['ven'] = {}
                        result['added'] = 1
                        for attr in tresult[0].items():
                            result['ven'][attr[0]] = attr[1]

                self.__output.append(result)

            # venue without pub
            elif len(result['pub']) == 0:
                result['alternative'] = []

                with self.pix.searcher(weighting=Frequency) as ps:
                    pq_parse = QueryParser('crossref', self.pix.schema).parse(result['ven']['key'])
                    tresult = ps.search(pq_parse, limit=None, )

                    if len(tresult):
                        plist = []
                        tmp = dict()
                        for el in tresult:
                            for attr in el.items():
                                if attr[0] == 'title':
                                    plist.append(attr[1])
                                    break

                        result['alternative'] = plist
                self.__output.append(result)

            # mixed case
            elif len(self.__output) == 0 or not result['ven']['key'] in [x['key'] for x in self.__output]:
                lis = [x for x in results if len(x['ven']) and x['ven']['key'] == result['ven']['key']]
                tmp = {}
                if len(lis) <= 1:
                    tmp = {'key': result['pub']['key'],
                           'score': result['score'],
                           'pub': [x['pub'] for x in lis],
                           'ven': result['ven'],
                           'alternative': list()}
                else:
                    tmp = {'key': result['ven']['key'],
                           'score': result['score'],
                           'pub': [x['pub'] for x in lis],
                           'ven': result['ven'],
                           'alternative': list()}
                plist = []
                with self.pix.searcher() as ps:
                    pq_parse = QueryParser('crossref', self.pix.schema).parse(tmp['key'])
                    tresult = ps.search(pq_parse, limit=None, )
                    if len(tresult):
                        for el in tresult:
                            for attr in el.items():
                                if attr[0] == 'title' and attr[1] not in [x['title'] for x in tmp['pub']]:
                                    plist.append(attr[1])
                                    break

                tmp['alternative'] = plist
                self.__output.append(tmp)

    def __ask_query(self):
        """ Get the user query to convert it in the whoosh supported query language."""
        self.__output = list()
        return input(form('What do you want to search?\n>  '))

    def __results(self, plist, vlist):
        """ Used at the end of the ranking function to mix the two indexes results and show only the relevants ones."""

        plist = sorted(plist, key=lambda s: s['score'], reverse=True)
        vlist = sorted(vlist, key=lambda s: s['score'], reverse=True)

        if len(plist) == 0:
            for el in vlist:
                el['key'] = el['ven']['key']
            results = vlist
        elif len(vlist) == 0:
            for el in plist:
                el['key'] = el['pub']['key']
            results = plist
        else:
            # cprint('QUI', 'red')
            results = tr(plist, vlist)

        # merge publications that have the same crossref
        same_venue = list()
        end_cycle = len(results)
        end_tot = 0
        for r in results:
            if end_tot >= end_cycle:
                break
            if len(r['pub']) and len(r['ven']):
                if len(same_venue):
                    id = None
                    f = False
                    for i in range(len(same_venue)):
                        if same_venue[i]['key'] == r['ven']['key']:
                            f = True  # found
                            id = i  # position
                            break
                    if not f:
                        same_venue.append({'key': r['ven']['key'], 'index': results.index(r)})
                    elif isinstance(results[id]['pub'], dict):  # create a new element
                        tmp = {'key': r['ven']['key'],
                               'score': r['pub']['o_score'] + results[same_venue[id]['index']]['score'],
                               'pub': [r['pub'],
                                       results[same_venue[id]['index']]['pub'], ], 'ven': r['ven'],
                               'alternative': [],}
                        del results[id]  # remove the id element and the actual element
                        results.remove(r)
                        results.append(tmp)  # add the element created
                        same_venue[id]['index'] = results.index(tmp)  # update the index
                        end_cycle -= 2 # due to the remotion of the 2 elements
                    else:
                        results[id]['pub'].append(r['pub'])
                        results[id]['score'] += r['pub']['o_score']
                        results.remove(r)
                        end_cycle -= 1  # due to the remotion of the element
                else:
                    same_venue.append({'key': r['ven']['key'], 'index': results.index(r)})

            end_tot += 1
        results = sorted(results, key=lambda s: s['score'], reverse=True)

        # find correlations
        if self.__output_level == 3:
            self.__find_correlations(results)
        else:
            self.__output = results

        cprint('RESULTS:', 'yellow', 'bold', 'url', start='\n\t', end='\n\n')
        count = 0
        for element in self.__output:
            if count == self.__result_limit:
                break
            q_print(element, count + 1, self.__output_level)
            count += 1

        self.__output = list()

    def bm25f(self, fuzzy):
        """ Used to get the rilevant documents. This ranking method use the default whoosh ranking method.
            If you want to use fuzzy search of the query terms set fuzzy=True"""

        pquery, vquery = to_whoosh_query(self.__ask_query())  # Get the query used in whoosh

        # ----------- PUBLICATIONS ----------------------
        with self.pix.searcher() as ps:
            # "" search for phrase in which the maximum distance between each word is 1
            # '' if you have to include characters in a term that are normally threated specially by the parsers, such
            #   as spaces, colons, or brackets.
            if fuzzy:
                pquery = MultifieldParser(['pubtype', 'author', 'title', 'year'], self.pix.schema,
                                          termclass=FuzzyTerm).parse(pquery)
            else:
                pquery = MultifieldParser(['pubtype', 'author', 'title', 'year'], self.pix.schema).parse(pquery)
            presults = ps.search(pquery, limit=None)

            cprint('Publications found: ' + str(len(presults)), 'bold', 'lightgrey', 'url', start='\n\t', end='\n')
            plist = []
            for el in presults:
                tmp = {'key': '', 'score': el.score, 'pub': {}, 'ven': {}, 'alternative': []}
                for attr in el.items():
                    tmp['pub'][attr[0]] = attr[1]
                tmp['pub']['o_score'] = tmp['score']
                plist.append(tmp)

        # --------------- VENUES --------------------------
        with self.vix.searcher() as vs:
            if fuzzy:
                vquery = MultifieldParser(['title', 'publisher'], self.vix.schema, termclass=FuzzyTerm).parse(vquery)
            else:
                vquery = MultifieldParser(['title', 'publisher'], self.vix.schema).parse(vquery)
            vresults = vs.search(vquery, limit=None)

            cprint('Venues found: ' + str(len(vresults)), 'bold', 'lightgrey', 'url', start='\t', end='\n')
            vlist = []
            for el in vresults:
                tmp = {'key': '', 'score': el.score, 'ven': {}, 'pub': {}, 'alternative': []}
                for attr in el.items():
                    tmp['ven'][attr[0]] = attr[1]
                tmp['ven']['o_score'] = tmp['score']
                vlist.append(tmp)
        self.__results(plist, vlist)  # Call the function to print the results.

    def frequency(self, fuzzy):
        """ Used to get the rilevant documents using the frequency of the searched terms in the document.
            If you want to use fuzzy search of the query terms set fuzzy=True"""

        pquery, vquery = to_whoosh_query(self.__ask_query())  # Get the query used in whoosh
        # Whoosh Frequency doesn't support the OR query, so it will be splitted to merge later.
        pquery = pquery.split(' OR ')
        vquery = vquery.split(' OR ')

        # ----------- PUBLICATIONS ----------------------
        with self.pix.searcher(weighting=Frequency) as ps:
            # "" search for phrase in which the maximum distance between each word is 1
            # '' if you have to include characters in a term that are normally threated specially by the parsers, such
            #   as spaces, colons, or brackets.
            presults = None
            for pq in pquery:
                if fuzzy:
                    pq_parse = QueryParser('title', self.pix.schema, termclass=FuzzyTerm).parse(pq)
                else:
                    pq_parse = QueryParser('title', self.pix.schema).parse(pq)

                if presults is not None:
                    tresult = ps.search(pq_parse, limit=None, )
                    presults.upgrade_and_extend(tresult)
                else:
                    presults = ps.search(pq_parse, limit=None, )

                if not pq.startswith(('title', 'author', 'year'), ):
                    if fuzzy:
                        pq_parse = QueryParser('author', self.pix.schema, termclass=FuzzyTerm).parse(pq)
                    else:
                        pq_parse = QueryParser('author', self.pix.schema).parse(pq)
                    tresult = ps.search(pq_parse, limit=None, )
                    presults.upgrade_and_extend(tresult)
                    if fuzzy:
                        pq_parse = QueryParser('year', self.pix.schema, termclass=FuzzyTerm).parse(pq)
                    else:
                        pq_parse = QueryParser('year', self.pix.schema).parse(pq)
                    tresult = ps.search(pq_parse, limit=None, )
                    presults.upgrade_and_extend(tresult)

            cprint('Publications found: ' + str(len(presults)), 'bold', 'lightgrey', 'url', start='\n\t', end='\n\n')
            plist = []
            for el in presults:
                tmp = {'key': '', 'score': el.score, 'pub': {}, 'ven': {}, }
                for attr in el.items():
                    tmp['pub'][attr[0]] = attr[1]
                plist.append(tmp)

        # --------------- VENUES --------------------------
        vresults = None
        with self.vix.searcher(weighting=Frequency) as vs:
            # print('1: ', vquery)
            for vq in vquery:
                # print('2: ', vq)
                if fuzzy:
                    vq_parse = QueryParser('title', self.vix.schema, termclass=FuzzyTerm).parse(vq)
                else:
                    vq_parse = QueryParser('title', self.vix.schema).parse(vq)
                if vresults is not None:
                    tresult = vs.search(vq_parse, limit=None)
                    vresults.upgrade_and_extend(tresult)
                else:
                    vresults = vs.search(vq_parse, limit=None)

                if not vq.startswith(('title:', 'publisher'), ):
                    if fuzzy:
                        vq_parse = QueryParser('publisher', self.vix.schema, termclass=FuzzyTerm).parse(vq)
                    else:
                        vq_parse = QueryParser('publisher', self.vix.schema).parse(vq)
                    tresult = vs.search(vq_parse, limit=None)
                    vresults.upgrade_and_extend(tresult)

            cprint('Venues found: ' + str(len(vresults)), 'bold', 'lightgrey', 'url', start='\t', end='\n')
            vlist = []
            for el in vresults:
                tmp = {'key': '', 'score': el.score, 'ven': {}, 'pub': {}, }
                for attr in el.items():
                    tmp['ven'][attr[0]] = attr[1]
                vlist.append(tmp)

        self.__results(plist, vlist)  # Call the function to print the results.
