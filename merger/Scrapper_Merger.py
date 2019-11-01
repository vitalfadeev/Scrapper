# 1. Load Conjugations
# 2. Load Wikipedia + Wikidata
# 3. Load Wiktionary
import os
import sqlite3
import logging
import logging.config
from Scrapper_DB import DBAddColumn, DBCheckStructure, DBExecuteScript, DBCheckIndex, DBCheckIndexes
from conjugator.Scrapper_Conjugations_Item import ConjugationsItem
from conjugator.Scrapper_Conjugator import DBConjugations
from merger.Scrapper_Merger_Item import WordItem
from wikidata.Scrapper_Wikidata import DBWikidata
from wikidata.Scrapper_Wikidata_Item import WikidataItem
from wikipedia.Scrapper_Wikipedia import DBWikipedia
from wikipedia.Scrapper_Wikipedia_Item import WikipediaItem
from wiktionary.Scrapper_Wiktionary import DBWikictionary
from wiktionary.Scrapper_Wiktionary_Item import WikictionaryItem

DBWord = sqlite3.connect( "word.db", timeout=5.0 )
log    = logging.getLogger(__name__)

# init DB
DBExecuteScript( DBWord, WordItem.Meta.DB_INIT )

if os.path.isfile( os.path.join( 'merger', 'logging.ini' ) ):
    logging.config.fileConfig( os.path.join( 'merger', 'logging.ini' ) )

#
from merger.Scrapper_Merger_Wikidata import load_wikidata
from merger.Scrapper_Merger_Conjugations import load_conjugations
from merger.Scrapper_Merger_Wikipedia import load_wikipedia
from merger.Scrapper_Merger_Wiktionary import load_wiktionary


def check_structure():
    # Wikidata
    #DBCheckStructure( DBWikidata, "wikidata", WikidataItem )

    DBCheckStructure( DBWikidata, "wikidata", {
        "Operation_Merging": "INTEGER NULL",
        "LabelNamePreference": "INTEGER NULL",
        "Operation_Pref": "INTEGER NULL",
    } )

    # Wikipedia
    DBCheckStructure( DBWikipedia, "wikipedia", {
        "Operation_Merging": "INTEGER NULL",
        "LabelNamePreference": "INTEGER NULL",
    } )

    # Wiktionary
    DBCheckStructure( DBWikictionary, "wiktionary", {
        "Operation_Merging": "INTEGER NULL",
        "LabelNamePreference": "INTEGER NULL",
    } )

    # Conjugations
    DBCheckStructure( DBConjugations, "conjugations", {
        "Operation_Merging": "INTEGER NULL",
        "LabelNamePreference": "INTEGER NULL",
    } )

    # Word
    DBWord = sqlite3.connect( "word.db", timeout=5.0 )
    DBCheckStructure( DBWord, "words", {
        "Operation_Merging": "INTEGER NULL",
        "Operation_Wikipedia": "INTEGER NULL",
        "LabelNamePreference": "INTEGER NULL",
    } )


def check_indexes_wikidata():
    DBCheckIndex( DBWikidata, "wikidata", "CodeInWiki" )


def check_indexes():
    # DBCheckIndex( DBWikipedia, "LabelTypeWP" )
    # DBCheckIndex( DBWikipedia, ["LabelTypeWP", "LabelType"] )
    # DBCheckIndex( DBWikipedia, ["LabelTypeWD", "LabelTypeWP", "LabelType"] )
    #
    # DBCheckIndexes( DBWikipedia, [
    #     "LabelTypeWP",
    #     ["LabelTypeWD", "LabelTypeWP", "LabelType"],
    # ] )

    DBCheckIndex( DBWord, "words", ["LanguageCode", "Ext_Wikipedia_URL", "LabelName"] )
    DBCheckIndex( DBWord, "words", ["LanguageCode", "LabelName"] )



def Set_Property_LabelNamePreference():
    # then divide by value of ( CAT-FELIDAE ) and divide by 2
    # If <0 then : =0 elif >1 then : =1

    # Wikipedia
    wp = WikipediaItem
    wps = \
        wp.SeeAlsoWikipediaLinks.count().sqrt() + \
        wp.ExplainationWPTxt.count().sqrt() + \
        wp.ExplainationTxt.len().sqrt()

    # then divide by value of ( CAT-FELIDAE ) and divide by 2
    # If <0 then : =0 elif >1 then : =1

    # Wiktionary
    wt = WikictionaryItem()
    wts = \
        0 - wt.IndexinPage * 3 + \
        wt.AlternativeFormsOther.count().sqrt() + \
        wt.Synonymy.count() + \
        wt.Antonymy.count() + \
        wt.Hypernymy.count() + \
        wt.Hyponymy.count() + \
        wt.Meronymy.count() + \
        wt.Translation_EN.count() + \
        wt.Translation_PT.count() + \
        wt.Translation_DE.count() + \
        wt.Translation_ES.count() + \
        wt.Translation_FR.count() + \
        wt.Translation_IT.count() + \
        wt.Translation_RU.count() + \
        wt.ExplainationExamplesTxt.count().sqrt() + \
        wt.ExplainationTxt.len().sqrt()
        # Check the codes in ExplainationRaw {{codes}} for special codes  (Rare=-25 , Obsolete=-25)

    # then divide by value of ( CAT-FELIDAE ) and divide by 2
    # If <0 then : =0 elif >1 then : =1

    # Verb conjugaison
    cj = ConjugationsItem()
    # then divide by value of ( THEY READ ) and divide by 2
    # If <0 then : =0 elif >1 then : =1

    # After done, set Field Operation_Pref=1


def main():
    check_structure()
    check_indexes_wikidata()

    # load 1
    load_wikidata()
    #load_conjugations()

    # create indexes
    check_indexes()

    # load 2
    #load_wikipedia()
    #load_wiktionary()

    # Vectorize



if __name__ == "__main__":
    main()
    # wd = ItemProxy( WikipediaItem() )
    # print( wd.ExplainationWPTxt.len() )
    # wd.ExplainationWPTxt = "123"
    # print( wd.ExplainationWPTxt.len() )
