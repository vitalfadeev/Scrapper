import logging
import sqlite3

from Scrapper_DB import DBRead, DBExecute, DBWrite
from Scrapper_IxiooAPI import Match_List_PKS_With_Lists_Of_PKS
from merger.Scrapper_Merger import DBWord
from merger.Scrapper_Merger_Item import WordItem
from wiktionary.Scrapper_Wiktionary_Item import WikictionaryItem

log    = logging.getLogger(__name__)


def merge_words( w, wt ):
    w.PK                        = wt.PrimaryKey
    w.SelfUrlWiktionary         = wt.SelfUrl
    w.LabelName                 = wt.LabelName
    w.LabelType                 = wt.LabelType
    w.LanguageCode              = wt.LanguageCode
    w.Type                      = wt.Type
    w.Description               = w.Description + '\n' * 3 + wt.ExplainationTxt + '\n'*3 + wt.DescriptionTxt
    w.ExplainationExamplesTxt  += wt.ExplainationExamplesTxt
    w.Synonymy                 += wt.Synonymy
    w.Antonymy                 += wt.Antonymy
    w.Hypernymy                += wt.Hypernymy
    w.Hyponymy                 += wt.Hyponymy
    w.Meronymy                 += wt.Meronymy
    w.Holonymy                 += wt.Holonymy
    w.Troponymy                += wt.Troponymy
    w.RelatedTerms             += wt.RelatedTerms
    w.RelatedTerms             += wt.Coordinate
    w.RelatedTerms             += wt.Otherwise
    w.AlsoKnownAs              += wt.AlternativeFormsOther
    # wt.DerivedTerms
    w.Translation_EN           += wt.Translation_EN
    w.Translation_FR           += wt.Translation_FR
    w.Translation_DE           += wt.Translation_DE
    w.Translation_IT           += wt.Translation_IT
    w.Translation_ES           += wt.Translation_ES
    w.Translation_RU           += wt.Translation_RU
    w.Translation_PT           += wt.Translation_PT
    w.IndexInPageWiktionary     = wt.IndexinPage

    if len( w.FromCJ ) == 0:
        w.IsMale           = wt.IsMale
        w.IsFeminine       = wt.IsFeminine
        w.IsNeutre         = wt.IsNeutre
        w.IsFeminine       = wt.IsSingle
        w.IsPlural         = wt.IsPlural
        w.SingleVariant    = wt.SingleVariant
        w.PluralVariant    = wt.PluralVariant
        w.PopularityOfWord = wt.PopularityOfWord
        w.MaleVariant      = wt.MaleVariant
        w.FemaleVariant    = wt.FemaleVariant
        w.IsVerbPast       = wt.IsVerbPast
        w.IsVerbPresent    = wt.IsVerbPresent
        w.IsVerbFutur      = wt.IsVerbFutur

    # wt.DescriptionWiktionaryLinks
    # wt.DescriptionWikipediaLinks
    # wt.DescriptionWikipediaLinks
    # wt.DescriptionWiktionaryLinks
    w.SeeAlso             += wt.SeeAlsoWiktionaryLinks
    w.SeeAlso             += wt.SeeAlsoWikipediaLinks

    w.FromWT.append( wt.PrimaryKey )


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
                 AND LabelName = ?          COLLATE NOCASE
                 AND FromWT is NULL """ # ci_index

    items = DBRead( DBWord, sql=sql, params=[wt.LanguageCode, wt.LabelName], cls=WordItem )
    items = list( items )

    if items:
        log.debug( "found items: %s", items )
        # Match_List_PKS_With_Lists_Of_PKS( explanations, translation_sentences )
        sentences1 = [ item.Description for item in items ]
        sentences2 = [ wt.ExplainationTxt ]

        log.debug( "matching:" )
        log.debug( "  sentences1: %s", sentences1 )
        log.debug( "  sentences2: %s", sentences2 )
        matches = Match_List_PKS_With_Lists_Of_PKS( tuple(sentences1), tuple(sentences2) )

        matched_words = [ item for (item, (s1, s2)) in zip(items, matches) if s2 == wt.ExplainationTxt ]

        if matched_words:
            # merge
            for w in matched_words:
                log.debug( "[ OK ] matched: %s == %s", w, wt )
                merge_words( w, wt )
                yield w

        else:
            # append
            log.debug( "new: %s", wt )
            w = WordItem()
            merge_words( w, wt )
            yield w

    else:
        # append
        log.debug( "new: %s", wt )
        w = WordItem()
        merge_words( w, wt )
        yield w


def load_wiktionary_one( lang, label ):
    with sqlite3.connect( "wiktionary.db", timeout=5.0 ) as DBWiktionary:
        with sqlite3.connect( "word.db", timeout=5.0 ) as DBWord:

            for wd in DBRead( DBWiktionary, table="wiktionary", cls=WikictionaryItem, where="LanguageCode=? COLLATE NOCASE AND LabelName=? COLLATE NOCASE", params=[ lang, label ] ):
                log.info( "%s", wd )

                for w in convert_wiktionary_to_word( wd ):
                    DBWrite( DBWord, w, table="words", if_exists="replace" )

                DBExecute( DBWiktionary, "UPDATE wiktionary SET Operation_Merging = 1 WHERE PrimaryKey = ?", wd.PrimaryKey )


def load_wiktionary():
    with sqlite3.connect( "wiktionary.db", timeout=5.0 ) as DBWiktionary:
        with sqlite3.connect( "word.db", timeout=5.0 ) as DBWord:

            #for wd in DBRead( DBWikipedia, table="wikipedia", cls=WikipediaItem ):
            for wd in DBRead( DBWiktionary, table="wiktionary", cls=WikictionaryItem, where="LanguageCode=? COLLATE NOCASE AND LabelName=? COLLATE NOCASE", params=["en", "Cat"] ):
                log.info( "%s", wd )

                for w in convert_wiktionary_to_word( wd ):
                    DBWrite( DBWord, w, table="words", if_exists="replace" )

                DBExecute( DBWiktionary, "UPDATE wiktionary SET Operation_Merging = 1 WHERE PrimaryKey = ?", wd.PrimaryKey )
