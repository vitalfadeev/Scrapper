import logging
import sqlite3

from Scrapper_DB import DBRead, DBExecute, DBWrite
from Scrapper_IxiooAPI import Match_List_PKS_With_Lists_Of_PKS
from _dev_scripts.v4.reader import read
from merger.Scrapper_Merger import DBWord
from merger.Scrapper_Merger_Item import WordItem
from wiktionary.Scrapper_Wiktionary_Item import WikictionaryItem

log    = logging.getLogger(__name__)


def merge_words( w, wt ):
    w.PK                           = wt.PrimaryKey
    w.LabelName                    = wt.LabelName
    w.LabelType                    = wt.LabelType
    w.LanguageCode                 = wt.LanguageCode
    w.Type                         = wt.Type
    w.IndexInPageWiktionary        = wt.IndexinPage
    w.Description                  = w.Description + '\n'*3 + wt.ExplainationTxt
    #w.ExplainationRaw             = wt.ExplainationRaw
    w.DescriptionWikipediaLinks    = wt.DescriptionWikipediaLinks
    w.DescriptionWiktionaryLinks   = wt.DescriptionWiktionaryLinks
    w.AlsoKnownAs                  += wt.AlternativeFormsOther
    w.SelfUrlWiktionary            = wt.SelfUrl
    w.Synonymy                     = wt.Synonymy
    w.Antonymy                     = wt.Antonymy
    w.Subclass_of                  += wt.Hypernymy
    w.Hyponymy                     = wt.Hyponymy
    w.Part_of                      += wt.Meronymy

    w.RelatedTerms                 += wt.RelatedTerms
    w.CoordinateTerms              += wt.Coordinate
    w.Otherwise                    += wt.Otherwise

    w.Translation_EN               += wt.Translation_EN
    w.Translation_FR               += wt.Translation_FR
    w.Translation_DE               += wt.Translation_DE
    w.Translation_IT               += wt.Translation_IT
    w.Translation_ES               += wt.Translation_ES
    w.Translation_RU               += wt.Translation_RU
    w.Translation_PT               += wt.Translation_PT

    w.ExplainationExamplesRaw      = wt.ExplainationExamplesRaw
    w.ExplainationExamplesTxt      = wt.ExplainationExamplesTxt

    w.IsMale                       = wt.IsMale
    w.IsFeminine                   = wt.IsFeminine
    w.IsNeutre                     = wt.IsNeutre
    w.IsSingle                     = wt.IsSingle
    w.IsPlural                     = wt.IsPlural
    w.SingleVariant                = wt.SingleVariant
    w.PluralVariant                = wt.PluralVariant
    w.MaleVariant                  = wt.MaleVariant
    w.FemaleVariant                = wt.FemaleVariant
    w.IsVerbPast                   = wt.IsVerbPast
    w.IsVerbPresent                = wt.IsVerbPresent
    w.IsVerbFutur                  = wt.IsVerbFutur
    w.VerbInfinitive               = ""
    w.VerbTense                    = ""
    #
    # w.Operation_Merging          = 0
    # w.Operation_Wikipedia        = 0
    # w.Operation_Vectorizer       = 0
    # w.Operation_PropertiesInv    = 0
    # w.Operation_VectSentences    = 0
    # w.Operation_Pref             = 0


def convert_wiktionary_to_word( wt: WikictionaryItem ) -> WordItem:
    # load all wiktionary
    # and merge with a existing word
    # if there is same labelname (not case sensitive),
    # then use PKS_ListMatch to see if we merge or not
    log.info( wt )

    # if same Ext_Wikipedia_URL
    sql = """ SELECT * 
                FROM words 
               WHERE LanguageCode = ?       COLLATE NOCASE
                 AND LabelName = ?          COLLATE NOCASE """ # ci_index

    items = DBRead( DBWord, sql=sql, params=[wt.LanguageCode, wt.LabelName], cls=WordItem )
    items = list( items )

    if items:
        # Match_List_PKS_With_Lists_Of_PKS( explanations, translation_sentences )
        sentences1 = [ item.ExplainationTxt for item in items ]
        sentences2 = [ wt.ExplainationTxt ]

        matches = Match_List_PKS_With_Lists_Of_PKS( tuple(sentences1), tuple(sentences2) )

        matched_words = [ item for (item, (s1, s2)) in zip(items, matches) if s2 == wt.ExplainationTxt ]

        if matched_words:
            # merge
            for w in matched_words:
                merge_words( w, wt )
                yield w

        else:
            # append
            w = WordItem()
            merge_words( w, wt )
            yield w

    else:
        # append
        w = WordItem()
        merge_words( w, wt )
        yield w


def load_wiktionary():
    with sqlite3.connect( "wiktionary.db", timeout=5.0 ) as DBWiktionary:
        with sqlite3.connect( "word.db", timeout=5.0 ) as DBWord:

            #for wd in DBRead( DBWikipedia, table="wikipedia", cls=WikipediaItem ):
            for wd in DBRead( DBWiktionary, table="wiktionary", cls=WikictionaryItem, where="LanguageCode=? COLLATE NOCASE AND LabelName=? COLLATE NOCASE", params=["en", "Cat"] ):
                log.info( "%s", wd )

                for w in convert_wiktionary_to_word( wd ):
                    DBWrite( DBWord, w, table="words", if_exists="fail" )

                DBExecute( DBWiktionary, "UPDATE wiktionary SET Operation_Merging = 1 WHERE PrimaryKey = ?", wd.PrimaryKey )
