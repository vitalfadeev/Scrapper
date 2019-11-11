import json
import logging

from Scrapper_DB import DBRead, DBExecute
from Scrapper_IxiooAPI import Vectorize_database_record, Vectorize_PKS
from wikidata.Scrapper_Wikidata_DB import DBWikidata
from wikipedia.Scrapper_Wikipedia_DB import DBWikipedia
from wiktionary.Scrapper_Wiktionary_DB import DBWiktionary

log = logging.getLogger(__name__)


def vectorize_properties_wikipedia():
    log.info( "Vectorizing wikipedia" )

    for wp in DBRead( DBWikipedia, sql=" SELECT * FROM wikipedia ", cls=dict ):

        log.info( "  vectorize: %s", wp["LabelName"] )

        vetorized = Vectorize_PKS( wp, default_language=wp["LanguageCode"] )

        DBExecute( DBWiktionary, """
            UPDATE wiktionary 
               SET
                   Description_Vect = ?,
                   AlsoKnownAs_Vect = ?,
                   Instance_of_Vect= ?,
                   Subclass_of_Vect = ?,
                   Part_of_Vect = ?,
                   Operation_Vectorizer = 1
             WHERE PrimaryKey = ?
             """,
                to_json( vetorized["Description"] ),
                to_json( vetorized["AlsoKnownAs"] ),
                to_json( vetorized["Instance_of"] ),
                to_json( vetorized["Subclass_of"] ),
                to_json( vetorized["Part_of"] ),
                wp["PrimaryKey"]
        )



def to_json( s ):
    if s is None:
        return None

    if isinstance( s, list ):
        return json.dumps( s, sort_keys=False, ensure_ascii=False )


def vectorize_properties_wiktionary():
    log.info( "Vectorizing wiktionary" )

    for wt in DBRead( DBWiktionary, sql=" SELECT * FROM wiktionary ", cls=dict ):

        log.info( "  vectorize: %s", wt["LabelName"] )

        vetorized = Vectorize_database_record( wt )

        DBExecute( DBWiktionary, """
            UPDATE wiktionary 
               SET
                   ExplainationTxt = ?,
                   AlternativeFormsOther_Vect = ?,
                   Synonymy_Vect = ?,
                   Antonymy_Vect = ?,
                   Hypernymy_Vect = ?,
                   Hyponymy_Vect = ?,
                   Meronymy_Vect = ?,
                   RelatedTerms_Vect = ?,
                   Coordinate_Vect = ?,
                   Otherwise_Vect = ?,
                   Operation_Vectorizer = 1
             WHERE PrimaryKey = ?
             """,
                to_json( vetorized["ExplainationTxt"] ),
                to_json( vetorized["AlternativeFormsOther"] ),
                to_json( vetorized["Synonymy"] ),
                to_json( vetorized["Antonymy"] ),
                to_json( vetorized["Hypernymy"] ),
                to_json( vetorized["Hyponymy"] ),
                to_json( vetorized["Meronymy"] ),
                to_json( vetorized["RelatedTerms"] ),
                to_json( vetorized["Coordinate"] ),
                to_json( vetorized["Otherwise"] ),
                wt["PrimaryKey"]
        )


def vectorize_properties_wikidata():
    log.info( "Vectorizing wikidata" )

    for wd in DBRead( DBWikidata, sql=" SELECT * FROM wikidata ", cls=dict ):

        log.info( "  vectorize: %s", wd["LabelName"] )

        vetorized = {}
        vetorized["Description"] = Vectorize_PKS( wd["Description"], default_language=wd["LanguageCode"] )
        vetorized["AlsoKnownAs"] = Vectorize_PKS( wd["AlsoKnownAs"], default_language=wd["LanguageCode"] )
        vetorized["Instance_of"] = Vectorize_PKS( wd["Instance_of"], default_language=wd["LanguageCode"] )
        vetorized["Subclass_of"] = Vectorize_PKS( wd["Subclass_of"], default_language=wd["LanguageCode"] )
        vetorized["Part_of"]     = Vectorize_PKS( wd["Part_of"], default_language=wd["LanguageCode"] )

        DBExecute( DBWikidata, """
            UPDATE wikidata
               SET
                   Description_Vect = ?,
                   AlsoKnownAs_Vect = ?,
                   Instance_of_Vect= ?,
                   Subclass_of_Vect = ?,
                   Part_of_Vect = ?,
                   Operation_Vectorizer = 1
             WHERE PrimaryKey = ?
             """,
                to_json( vetorized["Description"] ),
                to_json( vetorized["AlsoKnownAs"] ),
                to_json( vetorized["Instance_of"] ),
                to_json( vetorized["Subclass_of"] ),
                to_json( vetorized["Part_of"] ),
                wd["PrimaryKey"]
        )



def vectorize_properties():
    log.info( "Vectorizing" )
    vectorize_properties_wikipedia()
    #vectorize_properties_wiktionary()
    #vectorize_properties_wikidata()

