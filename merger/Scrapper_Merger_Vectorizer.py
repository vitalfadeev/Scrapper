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


def vectorize_properties_wiktionary():
    log.info( "Vectorizing wiktionary" )

    for wt in DBRead( DBWiktionary, sql=" SELECT * FROM wiktionary ", cls=dict ):

        log.info( "  vectorize: %s", wt["LabelName"] )

        vetorized = Vectorize_database_record( wt )

# [ ] AlternativeFormsOther
# [ ] Synonymy
# [ ] Antonymy
# [ ] Hypernymy
# [ ] Hyponymy
# [ ] Meronymy
# [ ] RelatedTerms
# [ ] Coordinate term
# [ ] Otherwise related

        DBExecute( DBWiktionary, """
            UPDATE wiktionary 
               SET  
                   Operation_Vectorizer = 1 
             WHERE PrimaryKey = ?
             """, wt["PrimaryKey"] )


def vectorize_properties():
    log.info( "Vectorizing" )
    #vectorize_properties_wikipedia()
    vectorize_properties_wiktionary()

