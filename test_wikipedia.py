from wikipedia import Scrapper_Wikipedia

if __name__ == "__main__":
    # Scrap all pages
    Scrapper_Wikipedia.scrap( lang="en", workers=4 )

    # Single page test
    # from Scrapper_DB import DBExecute, DBWrite
    # from wikipedia.Scrapper_Wikipedia import Page, scrap_one, DBWikipedia
    # lang = "en"
    # label = "Computer accessibility"
    # DBExecute( DBWikipedia, "DELETE FROM wikipedia WHERE LanguageCode = ? and LabelName = ?", lang, label )
    #
    # result = scrap_one( lang, Page( 0, 0, label, "", lang ) )
    #
    # for item in result:
    #     DBWrite( DBWikipedia, item )
