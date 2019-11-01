from Indexer.ixs_creation import Index
import whoosh.index as index
from os.path import abspath
from Support.TextFormat import cprint, form


def check_open_ixs():
    pix = index.open_dir('indexdir/PubIndex')
    vix = index.open_dir('indexdir/VenIndex')
    print('Indexes ok!')
    return pix, vix


def check_ixs():
    try:
        return check_open_ixs()
    except:
        while True:
            cprint('Indexes not found. Search Engine needs to create them.', 'orange', 'bold')
            db_path = input(form('Insert the DBLP file path: ', 'orange'))
            print()
            db_path = abspath(db_path)
            try:
                Index.create_ixs(Index(db_path))
            except:
                cprint('It seems there is an error with the path. Please retry', 'red', 'bold')
                continue
            try:
                return check_open_ixs()
            except:
                cprint('It seems there is an error.', 'red', 'bold')
            break