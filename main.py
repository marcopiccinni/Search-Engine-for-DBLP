from Support.TextFormat import form
import whoosh.index as index
from whoosh.qparser import QueryParser, MultifieldParser
from Indexer.ixs_creation import Index
import os

if __name__ == "__main__":

    make_choice = True
    while make_choice:
        choice = input('Do you want to create the indexes? [y/n]')
        if choice == 'y':
            make_choice = False
            Index.create_ixs(Index())
        elif choice == 'n':
            make_choice = False
        else:
            print(form('you MUST choice y or n', 'orange', 'bold'))

    """query tries """
    ix = index.open_dir('indexdir/PubIndex')
    vix = index.open_dir('indexdir/VenIndex')

    with ix.searcher() as searcher:
        query = MultifieldParser(['title', 'author'], ix.schema).parse('title:"computer science"')
        results = searcher.search(query)
        count = 1
        print('\n\t', form('Element found: ' + str(len(results)), 'bold', 'lightgrey', 'url'), end='\n\n')
        for element in results:
            print(form(str(count) + '.', 'red'))
            print(form(element['author'], 'lightblue'), end='')
            print(form(element['title'], 'yellow'))
            print('-' * 40)
            count += 1
