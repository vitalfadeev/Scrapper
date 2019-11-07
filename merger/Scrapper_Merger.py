# 1. Load Conjugations
# 2. Load Wikipedia + Wikidata
# 3. Load Wiktionary
import os
import logging
import logging.config

from merger.Scrapper_Merger_DB import DBWord
from Scrapper_DB import DBCheckStructure, DBCheckIndex
from conjugator.Scrapper_Conjugations_Item import ConjugationsItem
from conjugator.Scrapper_Conjugator_DB import DBConjugations
from wikidata.Scrapper_Wikidata_DB import DBWikidata
from wikipedia.Scrapper_Wikipedia_DB import DBWikipedia
from wikipedia.Scrapper_Wikipedia_Item import WikipediaItem
from wiktionary.Scrapper_Wiktionary_DB import DBWiktionary
from wiktionary.Scrapper_Wiktionary_Item import WiktionaryItem

from merger.Scrapper_Merger_Wikidata import load_wikidata, load_wikidata_one
from merger.Scrapper_Merger_Conjugations import load_conjugations, load_conjugations_one
from merger.Scrapper_Merger_Wikipedia import load_wikipedia, load_wikipedia_one
from merger.Scrapper_Merger_Wiktionary import load_wiktionary, load_wiktionary_one

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
        "Operation_Merging"    : "INTEGER NULL",
        "LabelNamePreference"  : "INTEGER NULL",
        "Operation_Pref"       : "INTEGER NULL",
        "Operation_Vectorizer" : "INTEGER NULL",
    } )

    # Wiktionary
    DBCheckStructure( DBWiktionary, "wiktionary", {
        "Operation_Merging"    : "INTEGER NULL",
        "LabelNamePreference"  : "INTEGER NULL",
        "Operation_Pref"       : "INTEGER NULL",
        "Operation_Vectorizer" : "INTEGER NULL",
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
        "MergedWith"                 : "TEXT NULL",
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


def main():
    # check_structure()
    # #
    # # # load 1
    # load_wikidata( DBWord )
    # load_conjugations( DBWord )
    #
    # # create indexes
    # check_indexes_wikidata()
    # check_indexes()
    #
    # # load 2
    # load_wikipedia( DBWord )
    # load_wiktionary( DBWord )

    # Vectorize
    #vectorize_properties()
    ...
