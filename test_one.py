import os
import sqlite3
import logging
from wiktionary import Scrapper_Wiktionary

log = logging.getLogger(__name__)


def setUp():
    # db
    Scrapper_Wiktionary.DBWikictionary.close()
    DB_NAME = "test_wiktionary.db"
    if os.path.isfile( DB_NAME ):
        os.remove( DB_NAME )
    Scrapper_Wiktionary.DB_NAME = DB_NAME
    Scrapper_Wiktionary.DBWikictionary = sqlite3.connect( DB_NAME, isolation_level=None )
    # init db
    Scrapper_Wiktionary.DBWikictionary.execute( "PRAGMA journal_mode = OFF" )
    Scrapper_Wiktionary.DBWikictionary.executescript(
        Scrapper_Wiktionary.WikictionaryItem.Meta.DB_INIT
    )


def get_test_file_content(lang, label):
    log.debug( "Current directory: " + os.getcwd() )

    with open(os.path.join('wiktionary', 'tests', lang , label + ".txt"), encoding="utf-8") as f:
        return f.read()

def scrap_one_test(lang="en", label="cat"):
    id_   = 0
    ns    = 0
    text  = get_test_file_content(lang, label)
    page  = Scrapper_Wiktionary.Page(id_, ns, label, text)
    items = Scrapper_Wiktionary.scrap_one( lang, page )
    return  items

if __name__ == "__main__":
    lang = 'en'
    title = 'quarter'

    setUp()
    items = scrap_one_test( lang, title )
