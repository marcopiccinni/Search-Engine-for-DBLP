# from whoosh.query import FuzzyTerm
from Support.TextFormat import cprint  # , form
from Support.TextArt import welcome_text, menu_text
from whoosh.qparser import MultifieldParser
# from whoosh import qparser
# import os
from Query.uquery import to_whoosh_query
from GUI.menu import check_ixs, Menu

if __name__ == "__main__":
    welcome_text('green', 'blink')
    menu_text('orange', 'bold')
    menu = Menu()
    #  menu.start()
    pix, vix = check_ixs()

    """query tries """

    # Interattivita' con utente

    # se io volessi cercare in AND con 'year' per trovare https://dblp.uni-trier.de/rec/xml/journals/kybernetes/Osimani14.xml?
    pquery, vquery = to_whoosh_query('publication.author:"Vianu" publication.year:2018 venue:VLDB')

    with pix.searcher() as ps:
        # "" search for phrase in which the maximum distance between each word is 1
        # '' if you have to include characters in a term that are normally threated specially by the parsers, such
        #   as spaces, colons, or brackets.
        pquery = MultifieldParser(['pubtype', 'author', 'title', 'year'], pix.schema).parse(pquery)
        # termclass=FuzzyTerm)
        presults = ps.search(pquery, limit=2)

        cprint('Element found[pub]: ' + str(len(presults)), 'bold', 'lightgrey', 'url', start='\n\t', end='\n\n')
        # plist = [{'score': el.score, 'pub': el.items()} for el in presults]
        plist = []
        for el in presults:
            tmp = {'score': el.score, 'pub': dict()}
            for attr in el.items():
                tmp['pub'][attr[0]] = attr[1]
            plist.append(tmp)

    with vix.searcher() as vs:
        query2 = MultifieldParser(['title', 'publisher'], vix.schema).parse(vquery)
        vresults = vs.search(query2, limit=2)

        cprint('Element found: ' + str(len(vresults)), 'bold', 'lightgrey', 'url', start='\n\t', end='\n\n')
        #        vlist = [{'score': el.score, 'ven': el.items()} for el in vresults]
        vlist = []
        for el in vresults:
            tmp = {'score': el.score, 'ven': dict()}
            for attr in el.items():
                tmp['ven'][attr[0]] = attr[1]
            vlist.append(tmp)

    from Ranking.Threshold import threshold_rank as tr

    for element in tr(plist, vlist):
        print('element = ', element)
