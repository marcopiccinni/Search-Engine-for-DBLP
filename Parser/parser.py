import xml.sax
from Support.TextFormat import cprint

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

    # -----------
    __CurrentElement = None
    writer = None

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
        cprint('Publication indexing started.\n', 'green')

    def endDocument(self):
        """Called when the parsing is completed"""
        cprint('Publication parsing completed.\n', 'green')

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

    # variable that defines a venue document
    isVenue = False

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
    parent = False

    # -----------
    __CurrentElement = None
    writer = None

    def __init__(self, writer):
        self.__reset(3)
        self.writer = writer
        super(VenueHandler, self).__init__()  # parent init

    def __reset(self, selector):
        """A function for resetting the class attributes.
            Selector is used for the bitwise and:
            1 to use first condition
            2 to use second condition
            3 to use both of them"""

        self.key = ''
        self.tag = ''

        if selector & 1:
            self.isVenue = False
            self.author = ''
            self.title = ''
            self.publisher = ''
            self.year = ''
            self.ee = ''
            self.url = ''

        if selector & 2:
            self.journal = ''
            self.parent = False

    def startDocument(self):
        """Called when the XML Parser starts reading the file"""
        cprint('Venue indexing started.\n', 'lightblue')

    def endDocument(self):
        """Called when the parsing is completed"""
        cprint('Venue indexing completed.\n', 'lightblue')

    def startElement(self, tag, attributes):
        """Called when a venue is parsed"""
        self.__CurrentElement = tag
        if tag in venue:
            for element_tag in venue:
                if tag == element_tag:
                    self.isVenue = True
                    self.key = str(attributes['key'])
                    self.tag = tag

        elif tag in publication:
            for element_tag in publication:
                if tag == element_tag:
                    self.parent = True
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
                                             )
                    self.__reset(1)

        if tag in publication:
            for element_tag in publication:
                if tag == element_tag:
                    self.writer.add_document(pubtype=self.tag,
                                             key=self.key,
                                             journal=self.journal
                                             )
                    self.__reset(2)

    def characters(self, content):
        """Called to assign the attributes of a venue document"""
        if self.isVenue:
            if self.__CurrentElement == "author":
                self.author += str(content)
            elif self.__CurrentElement == "title":
                self.title += str(content)
            elif self.__CurrentElement == "publisher":
                self.publisher += str(content)
            elif self.parent:
                if self.__CurrentElement == 'journal':
                    self.journal += content
            elif self.__CurrentElement == "ee":
                self.ee += str(content)
            elif self.__CurrentElement == "url":
                self.url += str(content)
            elif self.__CurrentElement == "year":
                self.year += str(content)
