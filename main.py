from Support.TextFormat import form
from Parser.parser import PublicationHandler, VenueHandler
from Indexer.index_schemas import create_schemas
from whoosh.index import create_in
import xml.sax
import os
import time
from multiprocessing import Process, cpu_count
from psutil import virtual_memory


def resources():
    """a function that returns kwargs for the index writer.
        We divided nproc and avaible_mem by 2 because
        we want to parallelize the code.
        'Perfectly balanced as everything should be'."""

    nproc = round(cpu_count() / 2)  # round for the case in which we have just 1 proc
    percentage_mem = 85 / 100
    available_mem = virtual_memory().available / 1024 ** 2 / 2  # in MB
    limitmb = round(available_mem / nproc * percentage_mem)

    return {'procs': nproc, 'limitmb': limitmb, 'multisegment': True}


def indexing(handler, schema, parser, db_path, index_path):
    """a function that handles the index creation"""
    index = create_in(index_path, schema)

    # ** returns dictionary as parameters
    writer = index.writer(**resources())

    parser.setContentHandler(handler(writer))
    parser.parse(db_path)
    writer.commit()


if __name__ == "__main__":
    # start = time.time()
    #
    # pub_schema, ven_schema = create_schemas()
    # index_main_dir = 'indexdir'
    # pub_index_path = 'indexdir/PubIndex'
    # ven_index_path = 'indexdir/VenIndex'
    # db_path = '/home/dani/Documents/Search-Engine-for-DBLP/db/dblp.xml'
    #
    # if not os.path.exists(index_main_dir):
    #     os.makedirs(index_main_dir)
    #
    # if not os.path.exists(pub_index_path):
    #     os.makedirs(pub_index_path)
    #
    # if not os.path.exists(ven_index_path):
    #     os.makedirs(ven_index_path)
    #
    # parser = xml.sax.make_parser()
    # parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    #
    # # PUBLICATIONS
    # t1 = Process(target=indexing, args=(PublicationHandler, pub_schema, parser, db_path, pub_index_path))
    # t1.start()
    #
    # # VENUE
    # t2 = Process(target=indexing, args=(VenueHandler, ven_schema, parser, db_path, ven_index_path))
    # t2.start()
    #
    # t1.join()
    # t2.join()
    # end = time.time()
    # print('Tempo totale: ', (end - start) / 60, ' minuti')

    import whoosh.index as index
    from whoosh.qparser import QueryParser

    ix = index.open_dir('indexdir/PubIndex')

    with ix.searcher() as searcher:
        query = QueryParser('author', ix.schema).parse('De Pretis')
        results = searcher.search(query)
        for element in results:
            print(form(element, 'green2'))
