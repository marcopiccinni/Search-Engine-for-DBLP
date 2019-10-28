from Parser.parser import PublicationHandler, VenueHandler
from Indexer.index_schemas import create_schemas
from whoosh.index import create_in
import xml.sax
import os
import time
from shutil import rmtree
from multiprocessing import Process, cpu_count
from psutil import virtual_memory
from Support.TextFormat import cprint


class Index:
    """Due to this class is called in the main file, the path begins to the main directory """
    index_main_dir = 'indexdir/'
    pub_index_path = 'indexdir/PubIndex'
    ven_index_path = 'indexdir/VenIndex'
    db_path = 'db/dblp.xml'

    def __init__(self, db_path=db_path):
        self.db_path = os.path.abspath(db_path)

    @staticmethod
    def __resources(self):
        """a function that returns kwargs for the index writer.
            We divided nproc and avaible_mem by 2 because we want to parallelize the indexing process.
            Indeed we create two index for the two types of documents so, the use of the resurces must be splitted for
            these two process.
            'Perfectly balanced as everything should be'."""

        nproc = round(cpu_count() / 2)  # round for the case in which we have just 1 proc
        percentage_mem = 85 / 100
        available_mem = virtual_memory().available / 1024 ** 2 / 2  # in MB
        limitmb = round(available_mem / nproc * percentage_mem)

        return {'procs': nproc, 'limitmb': limitmb, 'multisegment': True}

    def __indexing(self, handler, schema, parser, index_path):
        """a function that handles the index creation"""

        # ** returns dictionary as parameters
        writer = create_in(index_path, schema).writer(**self.__resources(self))

        parser.setContentHandler(handler(writer))
        parser.parse(self.db_path)

        if 'Pub' in index_path:
            cprint('Pubs commit started', 'green')
        else:
            cprint('Venues commit started', 'lightblue')

        writer.commit()

        if 'Pub' in index_path:
            cprint('Pubs commit ended', 'green')
        else:
            cprint('Venues commit ended', 'lightblue')

    def create_ixs(self):
        start = time.time()

        pub_schema, ven_schema = create_schemas()

        if os.path.exists(self.index_main_dir):
            rmtree(self.index_main_dir)

        os.makedirs(self.index_main_dir)
        os.makedirs(self.pub_index_path)
        os.makedirs(self.ven_index_path)

        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)

        # PUBLICATIONS
        t1 = Process(target=self.__indexing, args=(PublicationHandler, pub_schema, parser, self.pub_index_path))
        t1.start()

        # VENUE
        t2 = Process(target=self.__indexing, args=(VenueHandler, ven_schema, parser, self.ven_index_path, ))
        t2.start()

        t1.join()
        t2.join()
        end = time.time()
        print('Total time: ', round((end - start) / 60), ' minutes')
