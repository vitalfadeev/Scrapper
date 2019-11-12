import os
# from merger.Scrapper_Merger import check_structure, check_indexes_wikidata, check_indexes, merge
# from merger.Scrapper_Merger_Vectorizer import vectorize_properties

# def test_merge_one():
#     # Merge one
#     import os
#     if os.path.isfile("word.db"): os.remove("word.db")
#
#     #
#     lang = "en"
#     label = "cat"
#
#     # conjugations
#     from conjugator import Scrapper_Conjugator
#     from Scrapper_DB import DBWrite
#     Scrapper_Conjugator.DBDeleteLangRecords( lang )
#     page = Scrapper_Conjugator.get_one_verb_page( lang, label )
#     for item in Scrapper_Conjugator.scrap_one( lang, page ):
#         DBWrite( Scrapper_Conjugator.DBConjugations, item )
#
#     # wikipedia
#     from Scrapper_DB import DBExecute, DBWrite
#     from wikipedia import Scrapper_Wikipedia
#     from wikipedia.Scrapper_Wikipedia_RemoteAPI import get_wikitext
#     DBExecute( Scrapper_Wikipedia.DBWikipedia, "DELETE FROM wikipedia WHERE LanguageCode = ? and LabelName = ? COLLATE NOCASE", lang, label )
#
#     text = get_wikitext( label )
#     result = Scrapper_Wikipedia.scrap_one( lang, Scrapper_Wikipedia.Page( 0, 0, label, text, lang ) )
#
#     for item in result:
#         DBWrite( Scrapper_Wikipedia.DBWikipedia, item )
#
#     # merge
#     from merger import Scrapper_Merger
#     Scrapper_Merger.test_one( lang, label )


if __name__ == "__main__":
    # if os.path.isfile( "word.db" ): os.remove( "word.db" )
    from merger.Scrapper_Merger import merge
    lang = "en"
    merge( lang )
