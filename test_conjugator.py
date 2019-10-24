from conjugator import Scrapper_Conjugator
from conjugator.Scrapper_Conjugator import get_one_verb_page, scrap_one, DBDeleteLangRecords


def test_one( lang="en", label="do" ):
    result = DBDeleteLangRecords( lang )
    page = get_one_verb_page( lang, label )
    scrap_one( lang, page )


def test_all( lang="en", workers=1 ):
    Scrapper_Conjugator.scrap( workers=workers )


if __name__ == "__main__":
    #test_all("en", workers=1)
    test_one("en", "do")
