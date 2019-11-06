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
        # TODO: key: STORED? campo non per ricerca
        author=TEXT(stored=True, sortable=True),
        # TODO: author: Rimuovere sortable perchè non utilizzato
        title=TEXT(stored=True),
        pages=STORED,
        year=TEXT(sortable=True, stored=True),
        # TODO: year: Rimuovere sortable perchè non utilizzato.
        journal=TEXT(stored=True, sortable=True),
        # TODO: journal: Rimuovere sortable perchè non utilizzato.
        #                Solo STORED perchè campo non per ricerca.
        volume=STORED,
        number=STORED,
        url=STORED,
        ee=STORED,
        crossref=TEXT(stored=True)
        # TODO: crossref: Solo STORED perchè campo non per ricerca
    )

    ven_schema = Schema(
        pubtype=TEXT(stored=True),
        # TODO: pubtype: STORED? a differenza di "Pub" non è usato in ricerca
        key=ID(stored=True),
        # TODO: key: Solo STORED perchè campo non per ricerca
        author=TEXT(stored=True, sortable=True),
        # TODO: author: Rimuovere sortable perchè non utilizzato.
        #               Solo STORED perchè campo non per ricerca
        title=TEXT(stored=True),
        journal=TEXT(stored=True, sortable=True),
        # TODO: journal: Rimuovere sortable perchè non utilizzato.
        #                Solo STORED perchè campo non per ricerca
        publisher=TEXT(stored=True, sortable=True),
        # TODO: publisher: Rimuovere sortable perchè non utilizzato.
        url=STORED,
        ee=STORED,
        year=TEXT(sortable=True, stored=True),
        # TODO: year: Rimuovere sortable perchè non utilizzato.
        #             Solo STORED perchè campo non per ricerca
    )

    return pub_schema, ven_schema
