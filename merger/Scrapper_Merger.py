# 1. Load Conjugations
# 2. Load Wikipedia + Wikidata
# 3. Load Wiktionary
import os
import logging
import logging.config

from merger.Scrapper_Merger_DB import DBWord
from Scrapper_DB import DBCheckStructure, DBCheckIndex
from conjugator.Scrapper_Conjugator_DB import DBConjugations
from wikidata.Scrapper_Wikidata_DB import DBWikidata
from wikipedia.Scrapper_Wikipedia_DB import DBWikipedia
from wiktionary.Scrapper_Wiktionary_DB import DBWiktionary

from merger.Scrapper_Merger_Wikidata import load_wikidata, load_wikidata_one
from merger.Scrapper_Merger_Conjugations import load_conjugations, load_conjugations_one
from merger.Scrapper_Merger_Wikipedia import load_wikipedia, load_wikipedia_one
from merger.Scrapper_Merger_Wiktionary import load_wiktionary, load_wiktionary_one
from merger.Scrapper_Merger_Operations import operation_pref_wikidata, operation_pref, operation_pref_wiktionary, \
    operation_pref_wikipedia, operation_pref_conjugaison, calculate_they_read, calculate_cat_felidae

if os.path.isfile( os.path.join( 'merger', 'logging.ini' ) ):
    logging.config.fileConfig( os.path.join( 'merger', 'logging.ini' ) )

log    = logging.getLogger(__name__)


def check_structure():
    log.info( "checking structure" )

    # Wikidata
    #DBCheckStructure( DBWikidata, "wikidata", WikidataItem )

    DBCheckStructure( DBWikidata, "wikidata", {
        "Operation_Merging"   : "INTEGER NULL",
        "LabelNamePreference" : "INTEGER NULL",
        "Operation_Pref"      : "INTEGER NULL",
    } )

    # Wikipedia
    DBCheckStructure( DBWikipedia, "wikipedia", {
        "Operation_Merging"            : "INTEGER NULL",
        "LabelNamePreference"          : "INTEGER NULL",
        "Operation_Pref"               : "INTEGER NULL",
        "Operation_Vectorizer"         : "INTEGER NULL",
    } )

    # Wiktionary
    DBCheckStructure( DBWiktionary, "wiktionary", {
        "Operation_Merging"          : "INTEGER NULL",
        "LabelNamePreference"        : "INTEGER NULL",
        "Operation_Pref"             : "INTEGER NULL",
    } )

    # Conjugations
    DBCheckStructure( DBConjugations, "conjugations", {
        "Operation_Merging"   : "INTEGER NULL",
        "LabelNamePreference" : "INTEGER NULL",
        "Operation_Pref"      : "INTEGER NULL",
    } )

    # Word
    DBCheckStructure( DBWord, "words", {
        "Operation_Pref"             : "INTEGER NULL",
        "Operation_Merging"          : "INTEGER NULL",
        "Operation_Wikipedia"        : "INTEGER NULL",
        "Operation_Vectorizer"       : "INTEGER NULL",
        "LabelNamePreference"        : "INTEGER NULL",
        "MergedWith"                 : "TEXT NULL",

        "AlsoKnownAs_Vect"           : "TEXT NULL",
        "Instance_of_Vect"           : "TEXT NULL",
        "Subclass_of_Vect"           : "TEXT NULL",
        "Part_of_Vect"               : "TEXT NULL",
        "ExplainationTxt_Vect"       : "TEXT NULL",
        "AlternativeFormsOther_Vect" : "TEXT NULL",
        "Synonymy_Vect"              : "TEXT NULL",
        "Antonymy_Vect"              : "TEXT NULL",
        "Hypernymy_Vect"             : "TEXT NULL",
        "Hyponymy_Vect"              : "TEXT NULL",
        "Meronymy_Vect"              : "TEXT NULL",
        "RelatedTerms_Vect"          : "TEXT NULL",
        "CoordinateTerms_Vect"       : "TEXT NULL",
        "Otherwise_Vect"             : "TEXT NULL",

        "Description_Inv"            : "TEXT NULL",
        "AlsoKnownAs_Inv"            : "TEXT NULL",
        "Instance_of_Inv"            : "TEXT NULL",
        "Subclass_of_Inv"            : "TEXT NULL",
        "Part_of_Inv"                : "TEXT NULL",
        "ExplainationTxt_Inv"        : "TEXT NULL",
        "AlternativeFormsOther_Inv"  : "TEXT NULL",
        "Synonymy_Inv"               : "TEXT NULL",
        "Antonymy_Inv"               : "TEXT NULL",
        "Hypernymy_Inv"              : "TEXT NULL",
        "Hyponymy_Inv"               : "TEXT NULL",
        "Meronymy_Inv"               : "TEXT NULL",
        "RelatedTerms_Inv"           : "TEXT NULL",
        "CoordinateTerms_Inv"        : "TEXT NULL",
        "Otherwise_Inv"              : "TEXT NULL",
    } )


def check_indexes_wikidata():
    log.info( "checking wikidata indexes" )
    DBCheckIndex( DBWikidata, "wikidata", "CodeInWiki" )
    DBCheckIndex( DBWikidata, "wikidata", "LabelName" )
    DBCheckIndex( DBWikidata, "wikidata", "LanguageCode" )
    DBCheckIndex( DBWikidata, "wikidata", ["LanguageCode", 'LabelName'] )


def check_indexes():
    # DBCheckIndex( DBWikipedia, "LabelTypeWP" )
    # DBCheckIndex( DBWikipedia, ["LabelTypeWP", "LabelType"] )
    # DBCheckIndex( DBWikipedia, ["LabelTypeWD", "LabelTypeWP", "LabelType"] )
    #
    # DBCheckIndexes( DBWikipedia, [
    #     "LabelTypeWP",
    #     ["LabelTypeWD", "LabelTypeWP", "LabelType"],
    # ] )
    log.info( "checking words indexes" )

    DBCheckIndex( DBWord, "words",  ["LabelType"] )
    DBCheckIndex( DBWord, "words",  ["AlsoKnownAs"] )
    DBCheckIndex( DBWord, "words",  ["SelfUrlWikidata"] )
    DBCheckIndex( DBWord, "words",  ["SelfUrlWiktionary"] )
    DBCheckIndex( DBWord, "words",  ["SelfUrlWikipedia"] )

    DBCheckIndex( DBWord, "words", ["LanguageCode"] )
    DBCheckIndex( DBWord, "words", ["LabelName"] )
    DBCheckIndex( DBWord, "words", ["Ext_Wikipedia_URL"] )
    DBCheckIndex( DBWord, "words", ["Type"] )



def test_one( lang="en", label='Cat' ):
    check_structure()
    check_indexes_wikidata()

    # load 1
    load_wikidata_one( DBWord, lang, label )
    load_conjugations_one( DBWord, lang, label )

    # create indexes
    check_indexes()

    # load 2
    load_wikipedia_one( DBWord, lang, label )
    load_wiktionary_one( DBWord, lang, label )

    # Vectorize
    #vectorize_properties()


def merge( lang ):
    check_structure()
    calculate_cat_felidae()
    operation_pref_wikidata( lang )
    operation_pref_wiktionary( lang )
    operation_pref_wikipedia( lang )
    calculate_they_read()
    operation_pref_conjugaison( lang )

    # Merge all
    # merge
    load_wikidata( DBWord )
    load_conjugations( DBWord )

    # create indexes
    check_indexes_wikidata()
    check_indexes()

    # load 2
    load_wikipedia( DBWord )
    load_wiktionary( DBWord )
