import os
import sqlite3
import unittest
import itertools
import logging
from wiktionary import Scrapper_Wiktionary

log = logging.getLogger(__name__)


def get_test_file_content(lang, label):
    log.warning( "Current directory: " + os.getcwd() )

    with open(lang + "/" + label + ".txt", encoding="utf-8") as f:
        return f.read()


def scrap_one_test(lang="en", label="cat"):
    id_   = 0
    ns    = 0
    text  = get_test_file_content(lang, label)
    page  = Scrapper_Wiktionary.Page(id_, ns, label, text)
    items = Scrapper_Wiktionary.scrap_one( lang, page )
    return  items


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # db
        DB_NAME = "test_wiktionary.db"
        if os.path.isfile( DB_NAME ):
            os.remove( DB_NAME )
        Scrapper_Wiktionary.DB_NAME = DB_NAME
        Scrapper_Wiktionary.DBWikictionary = sqlite3.connect( DB_NAME, isolation_level=None )
        # init db
        Scrapper_Wiktionary.DBWikictionary.execute("PRAGMA journal_mode = OFF")
        Scrapper_Wiktionary.DBWikictionary.executescript(
            Scrapper_Wiktionary.WikictionaryItem.Meta.DB_INIT
        )


    def test_1_init(self):
        pass


    def test_2_en_cat(self):
        lang = 'en'
        title = 'cat'
        items = scrap_one_test( lang, title )

        self.assertIsInstance( items, list )

        # total count
        self.assertEqual( len(items), 30 )

        # total by type
        d = { k: len( list( group ) ) for k, group in itertools.groupby( items, lambda  x: x.IndexinToc.split('ex')[0] + x.Type ) }
        self.assertDictEqual( d,
                              { '1.2.1.noun'     : 14,
                                '1.2.2.verb'     : 5,
                                '1.3.1.noun'     : 1,
                                '1.4.1.noun'     : 1,
                                '1.4.2.verb'     : 2,
                                '1.5.1.adjective': 1,
                                '1.6.1.noun'     : 1,
                                '1.7.1.noun'     : 1,
                                '1.8.1.noun'     : 1,
                                '1.9.1.noun'     : 1,
                                '1.10.1.noun'    : 2
                               })


        # Translations
        # matches:
        #   1.2.1.ex.1. An animal of the family Felidae
        #   - member of the family Felidae
        #
        #   1.2.1.ex.1.1. A domesticated subspecies (Felis silvestris catus) of feline animal, commonly kept as a house pet.
        #   - domestic species
        #
        #   1.2.1.ex.1.2. Any similar animal of the family Felidae
        #   - member of the family Felidae
        #   - member of the family Felidae
        #   - member of the subfamily Felinae
        #
        #   1.2.1.ex.2. A person:
        #   1.2.1.ex.2.1. (offensive) A spiteful or angry woman
        #   -


        # Synonyms
        # d1 = { x.IndexinToc: len( x.Synonymy )  for x in items }


if __name__ == '__main__':
    unittest.main()

