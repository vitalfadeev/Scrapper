from conjugator import Scrapper_Conjugator
from conjugator.Scrapper_Conjugator import get_one_verb_page, scrap_one, DBDeleteLangRecords


def test_one( lang="en", label="do" ):
    result = DBDeleteLangRecords( lang )
    page = get_one_verb_page( lang, label )
    scrap_one( lang, page )


def test_all( lang="en", workers=1 ):
    Scrapper_Conjugator.scrap( lang=lang, workers=workers )


if __name__ == "__main__":
    #test_all( lang="en", workers=5 )
    #test_all( lang="fr", workers=5 )
    test_all( lang="de", workers=5 )
    test_all( lang="it", workers=5 )
    test_all( lang="es", workers=5 )
    test_all( lang="pt", workers=5 )
    test_all( lang="ru", workers=5 )
    #test_one("en", "do")

    #test_one("pt", "ir")

