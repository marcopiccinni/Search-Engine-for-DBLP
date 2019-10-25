from whoosh.query import FuzzyTerm
from Support.TextFormat import form
import whoosh.index as index
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import qparser
from Indexer.ixs_creation import Index
import os

if __name__ == "__main__":

    # make_choice = True
    # while make_choice:
    #     choice = input('Do you want to create the indexes? [y/n]')
    #     if choice == 'y':
    #         make_choice = False
    #         Index.create_ixs(Index())
    #     elif choice == 'n':
    #         make_choice = False
    #     else:
    #         print(form('you MUST choice y or n', 'orange', 'bold'))

    """query tries """
    ix = index.open_dir('indexdir/PubIndex')
    vix = index.open_dir('indexdir/VenIndex')

    with ix.searcher() as searcher:
        # "" search for phrase in which the maximum distance between each word is 1
        # '' if you have to include characters in a term that are normally threated specially by the parsers, such
        #   as spaces, colons, or brackets.
        query = qparser.QueryParser('title', ix.schema, termclass=FuzzyTerm)
        q = query.parse('computer science force')
        results = searcher.search(q, limit=5)
        count = 1

        # to show a pages (1 is the First page. Top 10 results
        # results = searcher.search_page(query, 1, pagelen=20)
        print('\n\t', form('Element found: ' + str(len(results)), 'bold', 'lightgrey', 'url'), end='\n\n')
        for element in results:
            print(form(str(count) + '.', 'red'), 'score = ', element.score)
            print(form(element['author'], 'lightblue'), end='')
            print(form(element['title'], 'yellow'))
            print('-' * 40)
            count += 1

    with vix.searcher() as s:
        query2 = MultifieldParser(['title', 'author'], vix.schema).parse('title:(computer science) OR author:(Denning)')
        # results2 = s.search_page(query2, 1)
        results2 = s.search(query2)
        print('\n\t', form('Element found: ' + str(len(results2)), 'bold', 'lightgrey', 'url'), end='\n\n')
        for element in results2:
            print(form(str(count) + '.', 'red'), 'score = ', element.score)
            print(form(element['author'], 'lightblue'), end='')
            print(form(element['title'], 'yellow'))
            print('-' * 40)
            count += 1

