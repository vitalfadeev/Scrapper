import logging
import sqlite3

from Scrapper_DB import DBWrite
from conjugator import Scrapper_Conjugator
from conjugator.Scrapper_Conjugator import get_one_verb_page, scrap_one, DBDeleteLangRecords
from conjugator.Scrapper_Conjugator_DB import DBConjugations

log = logging.getLogger(__name__)


def test_one( lang="en", label="do" ):
    result = DBDeleteLangRecords( lang )
    page = get_one_verb_page( lang, label )
    result = scrap_one( lang, page )

    for item in result:
        try:
            DBWrite( DBConjugations, item )
        except sqlite3.IntegrityError:
            log.warning( "PK: not unique: %s", item.PK )
            pass


def test_all( lang="en", workers=1 ):
    Scrapper_Conjugator.scrap( lang=lang, workers=workers )


if __name__ == "__main__":
    #test_all( lang="en", workers=5 )
    #test_all( lang="fr", workers=5 )
    #test_all( lang="de", workers=10 )
    #test_all( lang="it", workers=5 )
    #test_all( lang="es", workers=5 )
    #test_all( lang="pt", workers=5 )
    #test_all( lang="ru", workers=5 )
    #test_one("en", "do")

    test_one("en", "read")

