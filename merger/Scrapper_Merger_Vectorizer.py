import json
import logging

from Scrapper_DB import DBRead, DBExecute
from Scrapper_IxiooAPI import Vectorize_database_record
from wikipedia.Scrapper_Wikipedia_DB import DBWikipedia
from wiktionary.Scrapper_Wiktionary_DB import DBWiktionary

log = logging.getLogger(__name__)


def vectorize_properties_wikipedia():
    log.info( "Vectorizing wikipedia" )

    for wp in DBRead( DBWikipedia, sql=" SELECT * FROM wikipedia ", cls=dict ):

        log.info( "  vectorize: %s", wp["LabelName"] )

        vetorized = Vectorize_database_record( wp )


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
                to_json( vetorized["PrimaryKey"] ),
        )


def vectorize_properties():
    log.info( "Vectorizing" )
    #vectorize_properties_wikipedia()
    vectorize_properties_wiktionary()

