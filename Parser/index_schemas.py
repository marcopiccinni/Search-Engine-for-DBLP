from whoosh.fields import *


def create_schemas():
    # TEXT: the file is indexed, analyzed. By default it is not stored.
    #   Phrase=False does not allow to search for phrases.
    # ID: the file is indexed, without being analyzed.
    # STORED: the file is saved but not indexed.

    pub_schema = Schema(
        pubtype=TEXT(stored=True),
        key=ID(stored=True),
        author=TEXT(stored=True, phrase=False),
        title=TEXT(stored=True),
        pages=STORED,
        year=TEXT(phrase=False),
        journal=TEXT(stored=True),
        volume=STORED,
        number=STORED,
        url=STORED,
        ee=STORED,
        crossref=TEXT(stored=True)
    )

    venue_schema = Schema(
        pubtype=TEXT(stored=True),
        key=ID(stored=True),
        author=TEXT(stored=True, phrase=False),
        title=TEXT(stored=True),
        journal=TEXT(stored=True, phrase=False),
        publisher=TEXT(stored=True, phrase=False),
        url=STORED,
        ee=STORED
    )

    return pub_schema, venue_schema
