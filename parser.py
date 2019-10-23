import xml.sax
from whoosh.index import create_in
from whoosh.fields import *

publication = ['article', 'incollection', 'phdthesis', 'mastersthesis']
venue = ['book', 'inproceedings']


class PublicationHandler(xml.sax.ContentHandler):
    """Class for handle parsing events and adding documents to the publication index"""
    parentflag = False  # to check

    # attributes list
    key = ''
    tag = ''
    author = ''
    title = ''
    crossref = ''
    pages = ''
    year = ''

    # -----------
    __CurrentElement = None

    def __init__(self, writer):
        self.writer = writer
        super(PublicationHandler, self).__init__()  # parent init

    def startDocument(self):
        """Called when the XML Parser starts reading the file"""
        print('Publication indexing started.\n')

    def endDocument(self):
        """Called when the parsing is completed"""
        print('Parsing completed.\n')

    def startElement(self, tag, attributes):
        self.__CurrentElement = tag
        


    def endElement(self, tag):
