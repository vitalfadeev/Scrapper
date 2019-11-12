from wikipedia import Scrapper_Wikipedia
from wikipedia.Scrapper_Wikipedia_RemoteAPI import get_wikitext

if __name__ == "__main__":
    # Scrap all pages
    Scrapper_Wikipedia.scrap( lang="pt", workers=5 )

    # # Single page test
    # from Scrapper_DB import DBExecute, DBWrite
    # from wikipedia.Scrapper_Wikipedia import Page, scrap_one, DBWikipedia
    # lang = "en"
    # label = "Cat"
    # DBExecute( DBWikipedia, "DELETE FROM wikipedia WHERE LanguageCode = ? and LabelName = ? COLLATE NOCASE", lang, label )
    #
    # text = get_wikitext( label )
    # print(text)
    # result = scrap_one( lang, Page( 0, 0, label, text, lang ) )
    #
    # for item in result:
    #     DBWrite( DBWikipedia, item )

