import json
import logging
import sqlite3
from typing import Iterator

from Scrapper_DB import DBRead, DBExecute, DBWrite
from Scrapper_IxiooAPI import Match_List_PKS_With_Lists_Of_PKS
from merger.Scrapper_Merger_DB import DBWord
from merger.Scrapper_Merger_Item import WordItem
from wiktionary.Scrapper_Wiktionary_Item import WiktionaryItem
from wiktionary.Scrapper_Wiktionary_DB import DBWiktionary

log    = logging.getLogger(__name__)


def merge_words( w, wt ):
    w.PK                        = wt.PrimaryKey
    w.SelfUrlWiktionary         = wt.SelfUrl
    w.LabelName                 = wt.LabelName
    w.LabelType                 = wt.LabelType
    w.LanguageCode              = wt.LanguageCode
    w.Type                      = wt.Type

    if w.Description:
        w.Description          += '\n' * 3 + wt.DescriptionTxt
    else:
        w.Description          += wt.DescriptionTxt

    if wt.ExplainationExamplesTxt:
        w.ExplainationExamplesTxt.append( wt.ExplainationExamplesTxt )

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
        w.IsMale                = wt.IsMale
        w.IsFeminine            = wt.IsFeminine
        w.IsNeutre              = wt.IsNeutre
        w.IsFeminine            = wt.IsSingle
        w.IsPlural              = wt.IsPlural
        w.SingleVariant         = wt.SingleVariant
        w.PluralVariant         = wt.PluralVariant
        w.PopularityOfWord      = wt.PopularityOfWord
        w.MaleVariant           = wt.MaleVariant
        w.FemaleVariant         = wt.FemaleVariant
        w.IsVerbPast            = wt.IsVerbPast
        w.IsVerbPresent         = wt.IsVerbPresent
        w.IsVerbFutur           = wt.IsVerbFutur

    # wt.DescriptionWiktionaryLinks
    # wt.DescriptionWikipediaLinks
    # wt.DescriptionWikipediaLinks
    # wt.DescriptionWiktionaryLinks
    w.SeeAlso                  += wt.SeeAlsoWiktionaryLinks
    w.SeeAlso                  += wt.SeeAlsoWikipediaLinks

    w.FromWT.append( wt.PrimaryKey )


def update_MergedWith( wid, MergedWith, to ):
    MergedWith.append( to )
    MergedWith_str = json.dumps( MergedWith, ensure_ascii=False )
    DBExecute( DBWord, "UPDATE words SET MergedWith = ? WHERE PK = ?", MergedWith_str, wid )


def merge_verbs( wt: WiktionaryItem ) -> Iterator[WordItem ]:
    # 1. find verbs with same LaabelName, Type='verb'
    # 2. do PKS_Match_List
    # 3. merge matched

    # find same verbs
    sql = """ SELECT * 
                FROM words 
               WHERE LanguageCode = ?       COLLATE NOCASE
                 AND LabelName = ?          COLLATE NOCASE
                 AND Type = 'verb'          COLLATE NOCASE
                 AND FromWT is NULL """ # ci_index

    items = DBRead( DBWord, sql=sql, params=[wt.LanguageCode, wt.LabelName], cls=WordItem )
    items = list( items )

    #
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
                w.MergedWith.append( wt.PrimaryKey )
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



def merge_other( wt: WiktionaryItem ) -> Iterator[WordItem ]:
    # find same verbs
    sql = """ SELECT * 
                FROM words 
               WHERE LanguageCode = ?       COLLATE NOCASE
                 AND LabelName = ?          COLLATE NOCASE
                 AND Type <> 'verb'         COLLATE NOCASE
                 AND FromWT is NULL """ # ci_index

    items = DBRead( DBWord, sql=sql, params=[wt.LanguageCode, wt.LabelName], cls=WordItem )
    items = list( items )

    #
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
                w.MergedWith.append( wt.PrimaryKey )
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


def merge( wt: WiktionaryItem ) -> Iterator[WordItem ]:
    log.info( wt )

    if wt.Type == "verb":
        return merge_verbs( wt )
    else:
        return merge_other(wt )


def load_wiktionary_one( DBWord, lang, label ):
    for wd in DBRead( DBWiktionary, table="wiktionary", cls=WiktionaryItem, where="LanguageCode=? COLLATE NOCASE AND LabelName=? COLLATE NOCASE", params=[ lang, label ] ):
        log.info( "%s", wd )

        for w in merge( wd ):
            DBWrite( DBWord, w, table="words", if_exists="replace" )

        DBExecute( DBWiktionary, "UPDATE wiktionary SET Operation_Merging = 1 WHERE PrimaryKey = ?", wd.PrimaryKey )


def load_wiktionary( DBWord ):
    log.info( "loading wiktionary" )

    #for wd in DBRead( DBWikipedia, table="wikipedia", cls=WikipediaItem ):
    for wd in DBRead( DBWiktionary, table="wiktionary", cls=WiktionaryItem, where="LanguageCode=? COLLATE NOCASE AND LabelName=? COLLATE NOCASE", params=[ "en", "Cat" ] ):
        log.info( "%s", wd )

        for w in merge( wd ):
            DBWrite( DBWord, w, table="words", if_exists="replace" )

        DBExecute( DBWiktionary, "UPDATE wiktionary SET Operation_Merging = 1 WHERE PrimaryKey = ?", wd.PrimaryKey )
