import logging
import sqlite3

from Scrapper_DB import DBRead, DBWrite, DBExecute
from Scrapper_IxiooAPI import Match_List_PKS_With_Lists_Of_PKS
from merger.Scrapper_Merger import DBWord
from merger.Scrapper_Merger_Item import WordItem
from wikipedia.Scrapper_Wikipedia_Item import WikipediaItem

log = logging.getLogger( __name__ )


def merge_words( w, wp ):
    # LabelTypeWD/LabelTypeWP/LabelType:
    #   replace by priority: wikipedia, wiktionary, wikidata, conjugator
    # concatenate (keep Description) separate each with 3 \n
    # concatenate (keep AlsoKnownAs)

    w.PK                          = wp.PK
    w.LabelName                   = wp.LabelName
    w.LabelType                   = wp.LabelTypeWP
    w.LanguageCode                = wp.LanguageCode

    if w.Description:
        w.Description             = w.Description + '\n' * 3 + wp.ExplainationWPTxt
    else:
        w.Description             = wp.ExplainationWPTxt

    w.DescriptionWikipediaLinks  += wp.DescriptionWikipediaLinks
    w.DescriptionWiktionaryLinks += wp.DescriptionWiktionaryLinks
    w.SelfUrlWikipedia            = wp.SelfUrlWikipedia
    # w.SeeAlso                     = wp.SeeAlso  # disabled because http:// here
    w.SeeAlso                    += wp.SeeAlsoWikipediaLinks
    w.SeeAlso                    += wp.SeeAlsoWiktionaryLinks
    w.ExplainationExamplesTxt    += wp.ExplainationExamplesTxt

    w.FromWP.append( wp.PK )


def convert_wikipedia_to_word( wp: WikipediaItem ) -> WordItem:
    # load all wikipedia
    # and merge with exisiting word (wikidata)
    #   if same Ext_Wikipedia_URL,
    #   and also check if there is exisiting word with same labelname (not case sensitive),
    #   then use PKS_ListMatch to see if we merge or not

    log.info( wp )

    # search by URL and name
    sql = """ SELECT * 
                FROM words 
               WHERE LanguageCode = ?       COLLATE NOCASE
                 AND Ext_Wikipedia_URL = ?  COLLATE NOCASE 
                 AND LabelName = ?          COLLATE NOCASE """  # ci_index

    # do search
    items = DBRead( DBWord, sql=sql, params=[ wp.LanguageCode, wp.SelfUrlWikipedia, wp.LabelName ], cls=WordItem )
    items = list( items )

    #
    if items:
        # Match_List_PKS_With_Lists_Of_PKS( explanations, translation_sentences )
        sentences1 = [ item.ExplainationTxt for item in items ]
        sentences2 = [ wp.ExplainationWPTxt ]

        matches = Match_List_PKS_With_Lists_Of_PKS( tuple( sentences1 ), tuple( sentences2 ) )

        matched_words = [ item for (item, (s1, s2)) in zip( items, matches ) if s2 == wp.ExplainationWPTxt ]

        if matched_words:
            for w in matched_words:
                # merge
                merge_words( w, wp )
                yield w

        else:
            # append
            w = WordItem()
            merge_words( w, wp )
            yield w

    else:
        # append
        w = WordItem()
        merge_words( w, wp )
        w.PK            = wp.PK
        w.LabelName     = wp.LabelName
        w.LanguageCode  = wp.LanguageCode
        yield w


def load_wikipedia_one( lang, label ):
    with sqlite3.connect( "wikipedia.db", timeout=5.0 ) as DBWikipedia:
        with sqlite3.connect( "word.db", timeout=5.0 ) as DBWord:

            for wd in DBRead( DBWikipedia, table="wikipedia", cls=WikipediaItem, where="LanguageCode=? COLLATE NOCASE AND LabelName=? COLLATE NOCASE", params=[ lang, label ] ):
                log.info( "%s", wd )

                for w in convert_wikipedia_to_word( wd ):
                    DBWrite( DBWord, w, table="words", if_exists="fail" )

                DBExecute( DBWikipedia, "UPDATE wikipedia SET Operation_Merging = 1 WHERE PK = ?", wd.PK )


def load_wikipedia():
    with sqlite3.connect( "wikipedia.db", timeout=5.0 ) as DBWikipedia:
        with sqlite3.connect( "word.db", timeout=5.0 ) as DBWord:

            for wd in DBRead( DBWikipedia, table="wikipedia", cls=WikipediaItem ):
                log.info( "%s", wd )

                for w in convert_wikipedia_to_word( wd ):
                    DBWrite( DBWord, w, table="words", if_exists="fail" )

                DBExecute( DBWikipedia, "UPDATE wikipedia SET Operation_Merging = 1 WHERE PK = ?", wd.PK )

