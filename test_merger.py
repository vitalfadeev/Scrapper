import os
import logging
import logging.config

from merger.Scrapper_Merger import check_structure
from merger.Scrapper_Merger_Vectorizer import vectorize_properties

logging.config.fileConfig( os.path.join( 'merger', 'logging.ini' ) )


if __name__ == "__main__":
    # Merge all
    # merge
    # if os.path.isfile("word.db"): os.remove("word.db")
    # from merger import Scrapper_Merger
    # Scrapper_Merger.main()
    # exit(1)

    # from merger.Scrapper_Merger_Operations import calculate_cat_felidae
    # score = calculate_cat_felidae()
    # print( score )
    # exit(1)

    from merger.Scrapper_Merger_Operations import operation_pref_wikidata, operation_pref, operation_pref_wiktionary, \
    operation_pref_wikipedia, operation_pref_conjugaison, calculate_they_read

    check_structure()
    # score = operation_pref( "en" )
    # operation_pref_wiktionary( "en" )
    # operation_pref_wikipedia( "en" )
    # calculate_they_read()
    # operation_pref_conjugaison( "en" )

    vectorize_properties()
    exit(1)


    # Merge one
    import os
    if os.path.isfile("word.db"): os.remove("word.db")

    #
    lang = "en"
    label = "cat"

    # conjugations
    from conjugator import Scrapper_Conjugator
    from Scrapper_DB import DBWrite
    Scrapper_Conjugator.DBDeleteLangRecords( lang )
    page = Scrapper_Conjugator.get_one_verb_page( lang, label )
    for item in Scrapper_Conjugator.scrap_one( lang, page ):
        DBWrite( Scrapper_Conjugator.DBConjugations, item )

    # wikipedia
    from Scrapper_DB import DBExecute, DBWrite
    from wikipedia import Scrapper_Wikipedia
    from wikipedia.Scrapper_Wikipedia_RemoteAPI import get_wikitext
    DBExecute( Scrapper_Wikipedia.DBWikipedia, "DELETE FROM wikipedia WHERE LanguageCode = ? and LabelName = ? COLLATE NOCASE", lang, label )

    text = get_wikitext( label )
    result = Scrapper_Wikipedia.scrap_one( lang, Scrapper_Wikipedia.Page( 0, 0, label, text, lang ) )

    for item in result:
        DBWrite( Scrapper_Wikipedia.DBWikipedia, item )

    # merge
    from merger import Scrapper_Merger
    Scrapper_Merger.test_one( lang, label )

