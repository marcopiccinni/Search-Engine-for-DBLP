import xml.sax
from Support.TextFormat import form

publication = ['article', 'incollection', 'phdthesis', 'mastersthesis', 'inproceedings']
venue = ['book', 'proceedings']


class PublicationHandler(xml.sax.ContentHandler):
    """Class for handle parsing events and adding documents to the publication index"""

    # variable that defines if it is a publication
    isPublication = False

    # attributes list
    key = ''
    tag = ''
    author = ''
    title = ''
    crossref = ''
    pages = ''
    year = ''
    url = ''
    ee = ''
    journal = ''
    volume = ''
    number = ''

    # ----------- # TODO: Need a comment here?
    writer = None
    __CurrentElement = None

    def __init__(self, writer):
        self.__reset()
        self.writer = writer
        super(PublicationHandler, self).__init__()  # parent init

    def __reset(self):
        """A function for resetting the class attributes"""

        self.isPublication = False
        self.key = ''
        self.tag = ''
        self.author = ''
        self.title = ''
        self.crossref = ''
        self.pages = ''
        self.year = ''
        self.url = ''
        self.ee = ''
        self.journal = ''
        self.volume = ''
        self.number = ''

    def startDocument(self):
        """Called when the XML Parser starts reading the file"""

        print(form('Publication indexing started.', 'green'), flush=True)

    def endDocument(self):
        """Called when the parsing is completed"""

        print(form('Publication parsing completed.', 'green'), flush=True)

    def startElement(self, tag, attributes):
        """Called when a publication is parsed"""

        self.__CurrentElement = tag
        for element_tag in publication:
            if tag == element_tag:
                self.isPublication = True
                self.key = str(attributes['key'])
                self.tag = tag

    def endElement(self, tag):
        """Called when the parsing of the publication ends"""

        if self.tag == tag:
            self.writer.add_document(pubtype=self.tag,
                                     key=self.key,
                                     author=self.author,
                                     title=self.title,
                                     pages=self.pages,
                                     crossref=self.crossref,
                                     year=self.year,
                                     url=self.url,
                                     ee=self.ee,
                                     journal=self.journal,
                                     volume=self.volume,
                                     number=self.number, )

            self.__reset()

    def characters(self, content):
        """Called to assign the attributes of a publication document"""

        if self.isPublication:
            if self.__CurrentElement == 'author':
                self.author += str(content)
            elif self.__CurrentElement == "title":
                self.title += str(content)
            elif self.__CurrentElement == "pages":
                self.pages += str(content)
            elif self.__CurrentElement == "crossref":
                self.crossref += str(content)
            elif self.__CurrentElement == "year":
                self.year += str(content)
            elif self.__CurrentElement == "url":
                self.url += str(content)
            elif self.__CurrentElement == "ee":
                self.ee += str(content)
            elif self.__CurrentElement == "journal":
                self.journal += str(content)
            elif self.__CurrentElement == "volume":
                self.volume += str(content)
            elif self.__CurrentElement == "number":
                self.number += str(content)


class VenueHandler(xml.sax.ContentHandler):
    """Class for handle parsing events and adding documents to the venue index"""

    isVenue = False  # variable that defines a venue document

    # attributes list
    key = ''
    tag = ''
    author = ''
    title = ''
    journal = ''
    publisher = ''
    year = ''
    url = ''
    ee = ''
    isbn = ''
    parent = False

    # ----------- # TODO: Need a comment here?
    writer = None
    __CurrentElement = None

    def __init__(self, writer):
        self.__reset()
        self.writer = writer
        super(VenueHandler, self).__init__()  # parent init

    def __reset(self):
        """A function for resetting the class attributes."""

        self.key = ''
        self.tag = ''
        self.isVenue = False
        self.author = ''
        self.title = ''
        self.publisher = ''
        self.year = ''
        self.ee = ''
        self.url = ''
        self.isbn = ''
        self.journal = ''
        self.parent = False

    def startDocument(self):
        """Called when the XML Parser starts reading the file"""

        print(form('Venue indexing started.', 'lightcyan'), flush=True)

    def endDocument(self):
        """Called when the parsing is completed"""

        print(form('Venue indexing completed.', 'lightcyan'), flush=True)

    def startElement(self, tag, attributes):
        """Called when a venue is parsed"""

        self.__CurrentElement = tag

        if tag in venue:
            for element_tag in venue:
                if tag == element_tag:
                    self.isVenue = True
                    self.key = str(attributes['key'])
                    self.tag = tag

    def endElement(self, tag):
        """Called when the parsing of the venue ends"""

        if tag in venue:

            for element_tag in venue:
                if tag == element_tag:
                    self.writer.add_document(pubtype=self.tag,
                                             key=self.key,
                                             author=self.author,
                                             title=self.title,
                                             publisher=self.publisher,
                                             ee=self.ee,
                                             url=self.url,
                                             year=self.year,
                                             journal=self.journal,
                                             isbn=self.isbn,
                                             )
                    self.__reset()

    def characters(self, content):
        """Called to assign the attributes of a venue document"""

        if self.isVenue:
            if self.__CurrentElement == "author":
                self.author += str(content)
            elif self.__CurrentElement == "title":
                self.title += str(content)
            elif self.__CurrentElement == "publisher":
                self.publisher += str(content)
            # elif self.parent:
            elif self.__CurrentElement == 'journal':
                self.journal += content
            elif self.__CurrentElement == "ee":
                self.ee += str(content)
            elif self.__CurrentElement == "url":
                self.url += str(content)
            elif self.__CurrentElement == "year":
                self.year += str(content)
            elif self.__CurrentElement == "isbn":
                self.isbn += str(content)


if __name__ == '__main__':
    from Indexer.index_schemas import create_schemas
    from whoosh.index import create_in
    import xml.sax
    import os
    import time
    from shutil import rmtree
    from multiprocessing import Process, cpu_count
    from psutil import virtual_memory
    from Support.TextFormat import cprint


    def __resources():
        """a function that returns kwargs for the index writer.
            We divided nproc and avaible_mem by 2 because we want to parallelize the indexing process.
            Indeed we create two index for the two types of documents so, the use of the resurces must be splitted for
            these two process.
            'Perfectly balanced as everything should be'."""

        nproc = round(cpu_count())  # round for the case in which we have just 1 proc
        percentage_mem = 70 / 100
        available_mem = virtual_memory().available / 1024 ** 2   # in MB
        limitmb = round(available_mem / nproc * percentage_mem)

        return {'procs': nproc, 'limitmb': limitmb, 'multisegment': True}


    def __indexing(handler, schema, parser, index_path):
        """a function that handles the index creation"""

        # ** returns dictionary as parameters
        writer = create_in(index_path, schema).writer(**__resources())

        parser.setContentHandler(handler(writer))
        parser.parse(db_path)

        if 'Pub' in index_path:
            cprint('Pubs commit started', 'green')
        else:
            cprint('Venues commit started.', 'lightblue')

        writer.commit()

        if 'Pub' in index_path:
            cprint('Pubs commit ended.', 'green')
        else:
            cprint('Venues commit ended.', 'lightblue')


    index_main_dir = 'indexdir/'
    pub_index_path = 'indexdir/PubIndex'
    ven_index_path = 'indexdir/VenIndex'
    db_path = 'db/dblp.xml'

    start = time.time()

    pub_schema, ven_schema = create_schemas()

    if os.path.exists(index_main_dir):
        rmtree(index_main_dir)

    os.makedirs(index_main_dir)
    os.makedirs(pub_index_path)
    os.makedirs(ven_index_path)

    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # PUB
    __indexing(PublicationHandler, pub_schema, parser, pub_index_path)
    # VENUE
    __indexing(VenueHandler, ven_schema, parser, ven_index_path)
    # t2 = Process(target=__indexing, args=(VenueHandler, ven_schema, parser, ven_index_path,))
    # t2.start()
    #
    # t2.join()
    end = time.time()
    print('Total time: ', round((end - start) / 60), ' minutes')
