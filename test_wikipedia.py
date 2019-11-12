from wikipedia import Scrapper_Wikipedia
from wikipedia.Scrapper_Wikipedia_RemoteAPI import get_wikitext

if __name__ == "__main__":
    # Scrap all pages
    Scrapper_Wikipedia.scrap( lang="es", workers=10 )

    # # Single page test`
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

# https://michelanders.blogspot.com/2011/07/sqlite-multiprocessing-proxy-part-2.html
# https://www.reddit.com/r/learnpython/comments/3ml7zh/multiprocessing_and_sqlite3_how_to_handle/
# https://gist.github.com/filipkral/c51c6a78432706695f176dce0d2ac47a
# https://gist.github.com/cessor/f8bf530212fbe75263c79564f5fc15ad
# https://atomh.wordpress.com/2017/01/02/how-to-do-multiprocessingmulti-threading-in-python-with-sqlite/
# http://www.blog.pythonlibrary.org/2016/08/02/python-201-a-multiprocessing-tutorial/

# https://www.sqlite.org/faq.html#q5
