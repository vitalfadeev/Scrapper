import json
import logging

from Scrapper_DB import DBRead, DBExecute
from merger.Scrapper_Merger_DB import DBWord

log = logging.getLogger(__name__)


def invert_properties_words( lang ):
    log.info( "Vectorizing words" )

    for w in DBRead( DBWord, sql=" SELECT * FROM words ", cls=dict ):

        log.info( "  vectorize: %s", w["LabelName"] )

        vetorized = Vectorize_database_record( lang, w )

        DBExecute( DBWord, """
            UPDATE words 
               SET
                   ExplainationTxt_Vect = ?,
                   AlternativeFormsOther_Vect = ?,
                   Synonymy_Vect = ?,
                   Antonymy_Vect = ?,
                   Hypernymy_Vect = ?,
                   Hyponymy_Vect = ?,
                   Meronymy_Vect = ?,
                   RelatedTerms_Vect = ?,
                   Coordinate_Vect = ?,
                   Otherwise_Vect = ?,

                   Description_Vect = ?,
                   AlsoKnownAs_Vect = ?,
                   Instance_of_Vect= ?,
                   Subclass_of_Vect = ?,
                   Part_of_Vect = ?,

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

                to_json( vetorized["Description"] ),
                to_json( vetorized["AlsoKnownAs"] ),
                to_json( vetorized["Instance_of"] ),
                to_json( vetorized["Subclass_of"] ),
                to_json( vetorized["Part_of"] ),

                w["PrimaryKey"]
            )

def invert_properties( lang ):
    invert_properties_words( lang )

