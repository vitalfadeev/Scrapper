import logging
import sqlite3

from Scrapper_IxiooAPI import Match_List_PKS_With_Lists_Of_PKS
from _dev_scripts.v4.reader import read
from merger.Scrapper_Merger import DBWord
from merger.Scrapper_Merger_Item import WordItem
from wikipedia.Scrapper_Wikipedia_Item import WikipediaItem

log = logging.getLogger( __name__ )


def merge_words( w, wp ):
    # LabelTypeWD/LabelTypeWP/LabelType:
    #   replace by priority: wikipedia, wiktionary, wikidata, conjugator
    # concatenate (keep Description) separate each with 3 \n
    # concatenate (keep AlsoKnownAs)

    # w.PK                                        = wp.PK
    # w.LabelName                                 = wp.LabelName
    w.LabelType = wp.LabelTypeWP
    # w.LanguageCode                              = wp.LanguageCode
    w.ExplainationWPTxt = w.ExplainationWPTxt + '\n' * 3 + wp.ExplainationWPTxt
    w.ExplainationWPRaw = wp.ExplainationWPRaw
    w.DescriptionWikipediaLinks = wp.DescriptionWikipediaLinks
    w.DescriptionWiktionaryLinks = wp.DescriptionWiktionaryLinks
    w.DescriptionWikidataLinks = wp.DescriptionWikidataLinks
    w.SelfUrlWikipedia = wp.SelfUrlWikipedia
    w.SeeAlso = wp.SeeAlso
    w.SeeAlso.extends( wp.SeeAlsoWikipediaLinks )
    w.SeeAlsoWikipediaLinks = wp.SeeAlso
    # w.SeeAlsoWiktionaryLinks                    = wp.SeeAlsoWiktionaryLinks
    w.ExplainationExamplesRaw = wp.ExplainationExamplesRaw
    w.ExplainationExamplesTxt = wp.ExplainationExamplesTxt
    #
    # w.Operation_Merging                         = 0
    # w.Operation_Wikipedia                       = 0
    # w.Operation_Vectorizer                      = 0
    # w.Operation_PropertiesInv                   = 0
    # w.Operation_VectSentences                   = 0
    # w.Operation_Pref                            = 0


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
    items = read( DBWord, sql=sql, params=[ wp.LanguageCode, wp.SelfUrlWikipedia, wp.LabelName ], cls=WordItem ) \
        .as_list()

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
        yield w


def load_wikipedia():
    with sqlite3.connect( "wikipedia.db", timeout=5.0 ) as DBWikipedia:
        with sqlite3.connect( "word.db", timeout=5.0 ) as DBWord:
            read( DBWikipedia, table="wikipedia", cls=WikipediaItem ) \
                .generate( convert_wikipedia_to_word ) \
                .write( DBWord, table="words", if_exists="replace" )
