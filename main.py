from whoosh.query import FuzzyTerm
from Support.TextFormat import cprint, form
from Support.TextArt import welcome_text, menu_text
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import qparser
import os
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
    pquery, vquery = to_whoosh_query('publication:"Computer science" publication.title:2015')

    with pix.searcher() as searcher:
        # "" search for phrase in which the maximum distance between each word is 1
        # '' if you have to include characters in a term that are normally threated specially by the parsers, such
        #   as spaces, colons, or brackets.
        query = qparser.MultifieldParser(['pubtype', 'author', 'title', 'year'], pix.schema)  # termclass=FuzzyTerm)

        q = query.parse('"Spectre Attacks: "')
        presults = searcher.search(q, limit=1)
        count = 1
        cprint('Element found: ' + str(len(presults)), 'bold', 'lightgrey', 'url', start='\n\t', end='\n\n')
        for element in presults:
            print(form(str(count) + '.', 'red'), 'score = ', element.score)
            cprint(element['author'], 'lightblue', start='\t', end='')
            cprint(element['title'], 'yellow')
            print('-' * 40)
            count += 1

    with vix.searcher() as s:
        query2 = MultifieldParser(['title', 'author'], vix.schema).parse('title:(computer science) OR author:(Denning)')
        vresults = s.search(query2)
        cprint('Element found: ' + str(len(vresults)), 'bold', 'lightgrey', 'url', start='\n\t', end='\n\n')
        for element in vresults:
            print(form(str(count) + '.', 'red'), 'score = ', element.score)
            cprint(element['author'], 'lightblue', start='\t', end='')
            cprint(element['title'], 'yellow')
            print('-' * 40)
            count += 1
