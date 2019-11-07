import math
import re
import sqlite3
from functools import lru_cache

import nltk
from Scrapper_DB import DBRead, DBExecute
from wikidata.Scrapper_Wikidata_DB import DBWikidata
from merger.DBWikidata import WordItem
from merger.Scrapper_Merger_DB import DBWord
from wikidata.Scrapper_Wikidata_Item import WikidataItem
from wiktionary.Scrapper_Wiktionary_DB import DBWiktionary
from wiktionary.Scrapper_Wiktionary_Item import WiktionaryItem

nltk.download( 'punkt' )
from nltk import tokenize


# https://textminingonline.com/dive-into-nltk-part-ii-sentence-tokenize-and-word-tokenize
TOKENIZE_LANGS = {
    'en': 'english',
    'fr': 'french',
    'de': 'german',
    'it': 'italian',
    'es': 'spanish',
    'pt': 'portuguese',
    'ru': 'english',
}


def get_sentences( lang, text ):
    sentences = tokenize.sent_tokenize( text, language=TOKENIZE_LANGS[ lang ] )
    return sentences


def get_sentences_with_label( lang, text, label ):
    result = []

    #
    expecteds = re.split( "\W+" , label )
    lowered = list( map( str.lower, expecteds ) )
    cleaned_expected = ' ' + ' '.join( lowered ) + ' '  # is pattern for search

    #
    sentences = get_sentences( lang, text )

    for sentence in sentences:
        # lower
        lowered = sentence.lower()
        # remove [1]. [2], ...
        cleaned = re.sub( '\[[0-9]+\]', '', lowered )
        # 2. split sentence to words
        words = re.split( "\W+", cleaned )
        # to string
        cleaned_sentence = ' ' + ' '.join( words ) + ' '

        # 4. match
        # [ 'An' 'American' 'in' 'Paris' ] -> 'An American in Paris'
        if cleaned_expected in cleaned_sentence:
            result.append( sentence )

    return result


def calculate_rare_code_wktionary( wt ):
    # Check the codes in ExplainationRaw {{codes}} for special codes  (Rare=-25 , Obsolete=-25)
    score = 0

    ExplainationRaw_lower = wt.ExplainationRaw.lower()

    if ExplainationRaw_lower.find( "|obsolete}" ) != -1:
        score -= 25

    if ExplainationRaw_lower.find( "|rare}" ) != -1:
        score -= 25

    return 0


def calculate_preference_wiktionary( wt: WiktionaryItem ) -> float:
    #
    preference = \
        0 - wt.IndexinPage * 3 + \
        math.sqrt( len( wt.AlternativeFormsOther ) ) + \
        len( wt.Synonymy ) + \
        len( wt.Antonymy ) + \
        len( wt.Hypernymy ) + \
        len( wt.Hyponymy ) + \
        len( wt.Meronymy ) + \
        len( wt.Translation_EN ) + \
        len( wt.Translation_PT ) + \
        len( wt.Translation_DE ) + \
        len( wt.Translation_ES ) + \
        len( wt.Translation_FR ) + \
        len( wt.Translation_IT ) + \
        len( wt.Translation_RU ) + \
        len( wt.Translation_RU ) + \
        math.sqrt( len( wt.ExplainationExamplesTxt ) ) + \
        calculate_rare_code_wktionary( wt ) + \
        math.sqrt( len( wt.ExplainationTxt ) )

    return preference  # 27.517909943958315


@lru_cache(maxsize=2)
def calculate_cat_felidae():
    # 27.517909943958315

    DB_CAT = sqlite3.connect( "wiktionary-cat.db" )

    rows = DBRead( DB_CAT, sql = "SELECT * FROM wiktionary WHERE PrimaryKey = 'en-dictionary§Noun_Reference_Word_Alphabetical_with-1'", cls=WiktionaryItem )

    try:
        wt = next(rows)

    except StopIteration:
        raise Exception("No CAT-FELIDAE")

    DB_CAT.close()

    return calculate_preference_wiktionary( wt )


def operation_pref_wikidata( lang ):
    preference_base = calculate_cat_felidae()

    for wd in DBRead( DBWikidata, sql=" SELECT * FROM wikidata ", cls=WikidataItem ):

        ExplainationExamplesTxt = get_sentences_with_label( lang, wd.Description, wd.LabelName )
        ExplainationTxt = wd.Description

        preference = \
            len( wd.AlsoKnownAs ) + \
            len( wd.Instance_of ) + \
            len( wd.Subclass_of ) + \
            len( wd.Part_of ) + \
            len( wd.Translation_EN ) + \
            len( wd.Translation_PT ) + \
            len( wd.Translation_DE ) + \
            len( wd.Translation_ES ) + \
            len( wd.Translation_FR ) + \
            len( wd.Translation_IT ) + \
            len( wd.Translation_RU ) + \
            math.sqrt( wd.WikipediaLinkCountTotal ) + \
            math.sqrt( len( ExplainationExamplesTxt ) ) + \
            math.sqrt( len( ExplainationTxt ) )

        #
        # then divide by value of ( CAT-FELIDAE ) and divide by 2
        # If <0 then : =0 elif >1 then : =1

        #
        preference = preference / preference_base / 2

        if preference <= 0:
            LabelNamePreference = 0
        else:
            LabelNamePreference = 1

        DBExecute( DBWikidata, """
            UPDATE wikidata 
               SET LabelNamePreference = ? 
             WHERE PK = ?
             """, LabelNamePreference, wd.PK )


def operation_pref_wiktionary( lang ):
    preference_base = calculate_cat_felidae()

    for wt in DBRead( DBWikidata, sql=" SELECT * FROM wiktionary ", cls=WiktionaryItem ):

        preference = calculate_preference_wiktionary( wt )
        preference = preference / preference_base / 2

        if preference <= 0:
            LabelNamePreference = 0
        else:
            LabelNamePreference = 1

        DBExecute( DBWikidata, """
            UPDATE wiktionary 
               SET LabelNamePreference = ? 
             WHERE PK = ?
             """, LabelNamePreference, wt.PK )



def operation_pref( lang ):
    operation_pref_wikidata( lang )
