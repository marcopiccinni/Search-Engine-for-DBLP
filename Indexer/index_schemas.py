from whoosh.fields import *


def create_schemas():
    # TEXT: the file is indexed, analyzed. By default it is not stored.
    #   phrase=False does not allow to search for phrases.
    #   sortable=True  allows to sort the indexed values
    # ID: the file is indexed, without being analyzed.
    # STORED: the file is saved but not indexed.

    pub_schema = Schema(
        pubtype=TEXT(stored=True),
        key=ID(stored=True),
        author=TEXT(stored=True, phrase=False, sortable=True),
        title=TEXT(stored=True),
        pages=STORED,
        year=TEXT(phrase=False, sortable=True),
        journal=TEXT(stored=True, sortable=True),
        volume=STORED,
        number=STORED,
        url=STORED,
        ee=STORED,
        crossref=TEXT(stored=True)
    )

    venue_schema = Schema(
        pubtype=TEXT(stored=True),
        key=ID(stored=True),
        author=TEXT(stored=True, phrase=False, sortable=True),
        title=TEXT(stored=True),
        journal=TEXT(stored=True, phrase=False, sortable=True),
        publisher=TEXT(stored=True, phrase=False, sortable=True),
        url=STORED,
        ee=STORED
    )

    return pub_schema, venue_schema
