# 1. Load Conjugations
# 2. Load Wikipedia + Wikidata
# 3. Load Wiktionary
import sqlite3
import logging
from Scrapper_DB import DBAddColumn, DBCheckStructure, DBExecuteScript, DBCheckIndex, DBCheckIndexes
from Scrapper_Item import ItemProxy
from conjugator.Scrapper_Conjugations_Item import ConjugationsItem
from merger.Scrapper_Merger_Item import WordItem
from wikidata.Scrapper_Wikidata_Item import WikidataItem
from wikipedia.Scrapper_Wikipedia import DBWikipedia
from wikipedia.Scrapper_Wikipedia_Item import WikipediaItem
from wiktionary.Scrapper_Wiktionary_Item import WikictionaryItem
from merger import Scrapper_Merger_Wikidata

DBWord = sqlite3.connect( "word.db", timeout=5.0 )
log    = logging.getLogger(__name__)

# init DB
DBExecuteScript( DBWord, WordItem.Meta.DB_INIT )


def read( src ):
    ...


def load_conjugations():
    conjugations_db = "conjugations.db"

    read( conjugations_db )


def load_wikipedia():
    # load all wikipedia and merge with exisiting word (wikidata)
    #   if same Ext_Wikipedia_URL,
    #   and also check if there is exisiting word with same labelname (not case sensitive),
    #   then use PKS_ListMatch to see if we merge or not
    wikipedia_db = "wikipedia.db"
    wp = read( wikipedia_db )

    wikidata_db = "wikidata.db"
    wd = read( wikidata_db )

    # wd.select(
    #     wd.LabelName.lower() = wp.LabelName.lower() and
    #     wd.Ext_Wikipedia_URL = wp.Wikipedia_URL
    # )


def check_structure():
    # Wikipedia
    DBCheckStructure( DBWikipedia, "wikipedia", {
        "LabelNamePreference": "INTEGER NULL",
    } )

    # Word
    DBWord = sqlite3.connect( "word.db", timeout=5.0 )
    DBCheckStructure( DBWord, "word", {
        "Operation_Merging": "INTEGER NULL",
        "Operation_Wikipedia": "INTEGER NULL",
        "LabelNamePreference": "INTEGER NULL",
    } )
    DBCheckIndex( DBWikipedia, "LabelTypeWP" )
    DBCheckIndex( DBWikipedia, ["LabelTypeWP", "LabelType"] )
    DBCheckIndex( DBWikipedia, ["LabelTypeWD", "LabelTypeWP", "LabelType"] )

    DBCheckIndexes( DBWikipedia, [
        "LabelTypeWP",
        ["LabelTypeWD", "LabelTypeWP", "LabelType"],
    ] )


def Set_Property_LabelNamePreference():
    # Wikidata
    wd = ItemProxy( WikidataItem() )
    wds = sum(
        wd.AlsoKnownAs.count(),
        wd.Instance_of.count(),
        wd.Subclass_of.count(),
        wd.Part_of.count(),
        wd.Translation_EN.count(),
        wd.Translation_PT.count(),
        wd.Translation_DE.count(),
        wd.Translation_ES.count(),
        wd.Translation_FR.count(),
        wd.Translation_IT.count(),
        wd.Translation_RU.count(),
    )

    wd.WikipediaLinkCountTotal.sqrt()
    wd.ExplainationExamplesTxt.count().sqrt()
    wd.ExplainationTxt.len().sqrt()

    # then divide by value of ( CAT-FELIDAE ) and divide by 2
    # If <0 then : =0 elif >1 then : =1

    # Wikipedia
    wp = WikipediaItem
    wps = sum(
        wp.SeeAlsoWikipediaLinks.count().sqrt(),
        wp.ExplainationWPTxt.count().sqrt(),
        wp.ExplainationTxt.len().sqrt(),
    )
    # then divide by value of ( CAT-FELIDAE ) and divide by 2
    # If <0 then : =0 elif >1 then : =1

    # Wiktionary
    wt = WikictionaryItem()
    wts = sum(
        0 - wt.IndexinPage * 3,
        wt.AlternativeFormsOther.count().sqrt(),
        wt.Synonymy.count(),
        wt.Antonymy.count(),
        wt.Hypernymy.count(),
        wt.Hyponymy.count(),
        wt.Meronymy.count(),
        wt.Translation_EN.count(),
        wt.Translation_PT.count(),
        wt.Translation_DE.count(),
        wt.Translation_ES.count(),
        wt.Translation_FR.count(),
        wt.Translation_IT.count(),
        wt.Translation_RU.count(),
        wt.ExplainationExamplesTxt.count().sqrt(),
        # Check the codes in ExplainationRaw {{codes}} for special codes  (Rare=-25 , Obsolete=-25)
        wt.ExplainationTxt.len().sqrt(),
    )
    # then divide by value of ( CAT-FELIDAE ) and divide by 2
    # If <0 then : =0 elif >1 then : =1

    # Verb conjugaison
    cj = ConjugationsItem()
    cjs = sum(
        0
    )
    # then divide by value of ( THEY READ ) and divide by 2
    # If <0 then : =0 elif >1 then : =1

    # After done, set Field Operation_Pref=1


def merge():
    w = WordItem()
    wd = WikidataItem()
    wt = WikictionaryItem()
    wp = WikipediaItem()
    cj = ConjugationsItem()

    # Wikidata
    w.PK                             = wd.PrimaryKey
    w.LabelName                      = wd.LabelName
    w.LabelTypeWD                    = Scrapper_Merger_Wikidata.LabelTypeWD( wd )
    w.LanguageCode                   = wd.LanguageCode
    w.Description                    = wd.Description
    w.AlsoKnownAs                    = wd.AlsoKnownAs
    w.SelfUrlWikidata                = wd.SelfUrl
    w.Instance_of                    = Scrapper_Merger_Wikidata.Instance_of( wd )
    w.Subclass_of                    = Scrapper_Merger_Wikidata.Subclass_of( wd )
    w.Part_of                        = Scrapper_Merger_Wikidata.Part_of( wd )
    w.Translation_EN                 = wd.Translation_EN
    w.Translation_FR                 = wd.Translation_FR
    w.Translation_DE                 = wd.Translation_DE
    w.Translation_IT                 = wd.Translation_IT
    w.Translation_ES                 = wd.Translation_ES
    w.Translation_RU                 = wd.Translation_RU
    w.Translation_PT                 = wd.Translation_PT
    w.Ext_Wikipedia_URL              = Scrapper_Merger_Wikidata.Ext_Wikipedia_URL( wd )
    w.CountTotalOfWikipediaUrl       = Scrapper_Merger_Wikidata.CountTotalOfWikipediaUrl( wd )
    #
    # w.Operation_Merging              = 0
    # w.Operation_Wikipedia            = 0
    # w.Operation_Vectorizer           = 0
    # w.Operation_PropertiesInv        = 0
    # w.Operation_VectSentences        = 0
    # w.Operation_Pref                 = 0

    # Wiktionary
    w.PK                             = wt.PrimaryKey
    w.LabelName                      = wt.LabelName
    w.LabelType                      = wt.LabelType
    w.LanguageCode                   = wt.LanguageCode
    w.Type                           = wt.Type
    w.IndexInPageWiktionary          = wt.IndexinPage
    w.ExplainationTxt                = wt.ExplainationTxt
    w.ExplainationRaw                = wt.ExplainationRaw
    w.DescriptionWikipediaLinks      = wt.DescriptionWikipediaLinks
    w.DescriptionWiktionaryLinks     = wt.DescriptionWiktionaryLinks
    w.AlternativeFormsOther          = wt.AlternativeFormsOther
    w.SelfUrlWiktionary              = wt.SelfUrl
    w.Synonymy                       = wt.Synonymy
    w.Antonymy                       = wt.Antonymy
    w.Hypernymy                      = wt.Hypernymy
    w.Hyponymy                       = wt.Hyponymy
    w.Meronymy                       = wt.Meronymy
    w.RelatedTerms                   = wt.RelatedTerms
    w.CoordinateTerms                = wt.RelatedTerms
    w.Otherwise                      = wt.RelatedTerms
    w.Translation_EN                 = wt.Translation_EN
    w.Translation_FR                 = wt.Translation_FR
    w.Translation_DE                 = wt.Translation_DE
    w.Translation_IT                 = wt.Translation_IT
    w.Translation_ES                 = wt.Translation_ES
    w.Translation_RU                 = wt.Translation_RU
    w.Translation_PT                 = wt.Translation_PT
    w.ExplainationExamplesRaw        = wt.ExplainationExamplesRaw
    w.ExplainationExamplesTxt        = wt.ExplainationExamplesTxt
    w.IsMale                         = wt.IsMale
    w.IsFeminine                     = wt.IsFeminine
    w.IsNeutre                       = wt.IsNeutre
    w.IsSingle                       = wt.IsSingle
    w.IsPlural                       = wt.IsPlural
    w.SingleVariant                  = wt.SingleVariant
    w.PluralVariant                  = wt.PluralVariant
    w.MaleVariant                    = wt.MaleVariant
    w.FemaleVariant                  = wt.FemaleVariant
    w.IsVerbPast                     = wt.IsVerbPast
    w.IsVerbPresent                  = wt.IsVerbPresent
    w.IsVerbFutur                    = wt.IsVerbFutur
    w.VerbInfinitive                 = ""
    w.VerbTense                      = ""
    #
    # w.Operation_Merging              = 0
    # w.Operation_Wikipedia            = 0
    # w.Operation_Vectorizer           = 0
    # w.Operation_PropertiesInv        = 0
    # w.Operation_VectSentences        = 0
    # w.Operation_Pref                 = 0

    # Wikipedia
    w.PK                             = wp.PK
    w.LabelName                      = wp.LabelName
    w.LabelTypeWP                    = wp.LabelTypeWP
    w.LanguageCode                   = wp.LanguageCode
    w.ExplainationWPTxt              = wp.ExplainationWPTxt
    w.ExplainationWPRaw              = wp.ExplainationWPRaw
    w.DescriptionWikipediaLinks      = wp.DescriptionWikipediaLinks
    w.DescriptionWiktionaryLinks     = wp.DescriptionWiktionaryLinks
    w.DescriptionWikidataLinks       = wp.DescriptionWikidataLinks
    w.SelfUrlWikipedia               = wp.SelfUrlWikipedia
    w.SeeAlso                        = wp.SeeAlsoWikipediaLinks
    w.SeeAlsoWikipediaLinks          = wp.SeeAlso
    #w.SeeAlsoWiktionaryLinks         = wp.SeeAlsoWiktionaryLinks
    w.ExplainationExamplesRaw        = wp.ExplainationExamplesRaw
    w.ExplainationExamplesTxt        = wp.ExplainationExamplesTxt
    #
    # w.Operation_Merging              = 0
    # w.Operation_Wikipedia            = 0
    # w.Operation_Vectorizer           = 0
    # w.Operation_PropertiesInv        = 0
    # w.Operation_VectSentences        = 0
    # w.Operation_Pref                 = 0

    # Conjugations
    w.PK                             = cj.PK
    w.LabelName                      = cj.LabelName
    w.LabelType                      = cj.LabelType
    w.LanguageCode                   = cj.LanguageCode
    w.Type                           = cj.Type
    w.ExplainationTxt                = cj.ExplainationTxt
    w.AlternativeFormsOther          = cj.AlternativeFormsOther
    w.Otherwise                      = cj.OtherwiseRelated
    w.IsMale                         = cj.IsMale
    w.IsFeminine                     = cj.IsFeminine
    #w.IsNeutre                       = cj.IsNeutre
    w.IsSingle                       = cj.IsSingle
    w.IsPlural                       = cj.IsPlural
    w.IsVerbPast                     = cj.IsVerbPast
    w.IsVerbPresent                  = cj.IsVerbPresent
    w.IsVerbFutur                    = cj.IsVerbFutur


def load_wikidata():
    read( WikidataDB ).conver().write( WDB )
    read( ConjugationsDB ).conver().write( WDB )
    read( WikipediaDB ).conver( merge_wikipedia_with_wikidata ).write( WDB ) # if same pk - overwrite
    read( WiktionaryDB ).conver( merge_wiktionary_with_wikidata ).write( WDB )


def main():
    check_structure()
    load_wikidata()


if __name__ == "__main__":
    main()
    # wd = ItemProxy( WikipediaItem() )
    # print( wd.ExplainationWPTxt.len() )
    # wd.ExplainationWPTxt = "123"
    # print( wd.ExplainationWPTxt.len() )
