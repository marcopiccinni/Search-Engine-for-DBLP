from whoosh.fields import *


def create_schemas():
    """define the schema for the pubs and the venues"""

    # TEXT: the field is indexed, analyzed. By default it is not stored.
    # phrase=False does not allow to search for phrases.
    # sortable=True  allows to sort the indexed values
    # ID: the file is indexed, without being analyzed.
    # STORED: the file is saved but not indexed.

    pub_schema = Schema(
        pubtype=TEXT(stored=True),
        key=STORED,
        author=TEXT(stored=True),
        title=TEXT(stored=True),
        pages=STORED,
        year=TEXT(stored=True),
        journal=STORED,
        volume=STORED,
        number=STORED,
        url=STORED,
        ee=STORED,
        crossref=ID(stored=True),
    )

    ven_schema = Schema(
        pubtype=STORED,
        key=ID(stored=True),
        author=STORED,
        title=TEXT(stored=True),
        journal=STORED,
        publisher=TEXT(stored=True),
        url=STORED,
        ee=STORED,
        year=STORED,
        isbn=STORED,
    )

    return pub_schema, ven_schema
