import logging
import sqlite3

from Scrapper_DB import DBRead, DBWrite, DBExecute
from conjugator.Scrapper_Conjugations_Item import ConjugationsItem
from merger.Scrapper_Merger_Item import WordItem

log    = logging.getLogger(__name__)


def convert_conjugations_to_word( c: ConjugationsItem ) -> WordItem:
    log.info( c )

    w = WordItem()

    w.PK                             = c.PK
    w.LabelName                      = c.LabelName
    w.LabelType                      = c.LabelType
    w.LanguageCode                   = c.LanguageCode
    w.Type                           = c.Type
    w.ExplainationTxt                = c.ExplainationTxt
    w.AlternativeFormsOther          = c.AlternativeFormsOther
    w.Otherwise                      = c.OtherwiseRelated
    w.IsMale                         = c.IsMale
    w.IsFeminine                     = c.IsFeminine
    #w.IsNeutre                       = c.IsNeutre
    w.IsSingle                       = c.IsSingle
    w.IsPlural                       = c.IsPlural
    w.IsVerbPast                     = c.IsVerbPast
    w.IsVerbPresent                  = c.IsVerbPresent
    w.IsVerbFutur                    = c.IsVerbFutur

    return w


def load_conjugations():
    with sqlite3.connect( "conjugations.db", timeout=5.0 ) as DBConjugations:
        with sqlite3.connect( "word.db", timeout=5.0 ) as DBWord:

#            for wd in DBRead( DBConjugations, table="conjugations", cls=ConjugationsItem ):
            for wd in DBRead( DBConjugations, table="conjugations", cls=ConjugationsItem, where="LanguageCode=? COLLATE NOCASE AND LabelName=? COLLATE NOCASE", params=["en", "Cat"] ):
                log.info( "%s", wd )

                w = convert_conjugations_to_word( wd )
                DBWrite( DBWord, w, table="words", if_exists="fail" )

                DBExecute( DBConjugations, "UPDATE conjugations SET Operation_Merging = 1 WHERE PK = ?", 1 )

