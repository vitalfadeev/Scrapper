import json
import logging
import logging.config
import os

from Scrapper_DB import DBRead, DBExecute
from Scrapper_IxiooAPI import Vectorize_database_record, Vectorize_PKS
from merger.DBWikidata import WordItem
from merger.Scrapper_Merger_DB import DBWord
from wikidata.Scrapper_Wikidata_DB import DBWikidata
from wikipedia.Scrapper_Wikipedia_DB import DBWikipedia
from wiktionary.Scrapper_Wiktionary_DB import DBWiktionary

if os.path.isfile( os.path.join( 'vectorizer', 'logging.ini' ) ):
    logging.config.fileConfig( os.path.join( 'vectorizer', 'logging.ini' ) )

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


def vectorize_properties_words( lang ):
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

                w["PK"]
            )


def get_inv_prop_name( prop ):
    if prop.lower().endswith( "_vect" ):
        prop = prop[ :-len("_vect") ]
    return prop + "_Inv"


def add_inv_prop_value( word, prop, value ):
    inv_prop = get_inv_prop_name( prop )
    setattr( word, inv_prop, value )


def find_word_by_label( label ):
    sql = """
        SELECT * 
          FROM words 
    """
    rows = DBRead( DBWord, sql=sql )

    return ''


def invert_property( lang, word, prop ):
    # 1. take word
    # 2. get description
    # 3.   on each description word:
    #      - find word
    #      - add to description_inv self.PK
    # ('description' is example and can be any '*_Vect' property)
    value = getattr( word, prop )
    words = get_words( value )

    for w in words:
        w2 = find_word_by_label( w.LabelName )
        add_inv_prop_value( w2, prop, w.LabelName )


def invert_vector_properties( lang ):
    # 1. PK -> Description[ PK1, PK2, ... ]
    # 2. PK1 -> Description_Inv[ ..., PK ]
    #    PK2 -> Description_Inv[ ..., PK ]
    log.info( "Invert vectors words" )

    word = WordItem()
    properties_to_invert = [ x for x in vars(word) if not callable(x) and x.endswith("_Vect") ]

    for w in DBRead( DBWord, sql=" SELECT * FROM words ", cls=dict ):

        log.info( "  invert vector: %s", w["LabelName"] )

        for prop in properties_to_invert:
            inverted = invert_property( lang, w, prop )

        # DBExecute( DBWord, """
        #     UPDATE words
        #        SET
        #            ExplainationTxt_Vect = ?,
        #            AlternativeFormsOther_Vect = ?,
        #            Synonymy_Vect = ?,
        #            Antonymy_Vect = ?,
        #            Hypernymy_Vect = ?,
        #            Hyponymy_Vect = ?,
        #            Meronymy_Vect = ?,
        #            RelatedTerms_Vect = ?,
        #            Coordinate_Vect = ?,
        #            Otherwise_Vect = ?,
        #
        #            Description_Vect = ?,
        #            AlsoKnownAs_Vect = ?,
        #            Instance_of_Vect= ?,
        #            Subclass_of_Vect = ?,
        #            Part_of_Vect = ?,
        #
        #            Operation_Vectorizer = 1
        #      WHERE PrimaryKey = ?
        #      """,
        #         to_json( vetorized["ExplainationTxt"] ),
        #         to_json( vetorized["AlternativeFormsOther"] ),
        #         to_json( vetorized["Synonymy"] ),
        #         to_json( vetorized["Antonymy"] ),
        #         to_json( vetorized["Hypernymy"] ),
        #         to_json( vetorized["Hyponymy"] ),
        #         to_json( vetorized["Meronymy"] ),
        #         to_json( vetorized["RelatedTerms"] ),
        #         to_json( vetorized["Coordinate"] ),
        #
        #         to_json( vetorized["Description"] ),
        #         to_json( vetorized["AlsoKnownAs"] ),
        #         to_json( vetorized["Instance_of"] ),
        #         to_json( vetorized["Subclass_of"] ),
        #         to_json( vetorized["Part_of"] ),
        #
        #         w["PrimaryKey"]
        #     )


def vectorize_properties( lang ):
    log.info( "Vectorizing" )
    vectorize_properties_words( lang )
    invert_vector_properties( lang )

