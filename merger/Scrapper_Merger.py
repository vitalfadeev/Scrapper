# 1. Load Conjugations
# 2. Load Wikipedia + Wikidata
# 3. Load Wiktionary
import sqlite3
import logging
from Scrapper_DB import DBAddColumn, DBCheckStructure, DBExecuteScript, DBCheckIndex, DBCheckIndexes
from Scrapper_Item import ItemProxy
from conjugator.Scrapper_Conjugations_Item import ConjugationsItem
from merger.Scrapper_Merger_Conjugations import load_conjugations
from merger.Scrapper_Merger_Item import WordItem
from merger.Scrapper_Merger_Wikidata import load_wikidata
from merger.Scrapper_Merger_Wikipedia import load_wikipedia
from merger.Scrapper_Merger_Wiktionary import load_wiktionary
from wikidata.Scrapper_Wikidata import DBWikidata
from wikidata.Scrapper_Wikidata_Item import WikidataItem
from wikipedia.Scrapper_Wikipedia import DBWikipedia
from wikipedia.Scrapper_Wikipedia_Item import WikipediaItem
from wiktionary.Scrapper_Wiktionary_Item import WikictionaryItem

DBWord = sqlite3.connect( "word.db", timeout=5.0 )
log    = logging.getLogger(__name__)

# init DB
DBExecuteScript( DBWord, WordItem.Meta.DB_INIT )


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
    DBCheckIndex( DBWikidata, "wikidata", "CodeInWiki" )



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


def main():
    # check_structure()

    # load 1
    load_wikidata()
    #load_conjugations()

    # create indexes
    check_indexes()

    # load 2
    #load_wikipedia()
    #load_wiktionary()


if __name__ == "__main__":
    main()
    # wd = ItemProxy( WikipediaItem() )
    # print( wd.ExplainationWPTxt.len() )
    # wd.ExplainationWPTxt = "123"
    # print( wd.ExplainationWPTxt.len() )
