import math
import re
from functools import lru_cache

import nltk
from Scrapper_DB import DBRead, DBExecute
from merger.DBWikidata import WordItem
from merger.Scrapper_Merger import DBWord
from wiktionary.Scrapper_Wiktionary import DBWiktionary
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


@lru_cache
def get_preference( wid ):
    # Noun_Felidae_Cougar_Puma_Lynx
    rows = DBRead( DBWiktionary, sql=""" 
        SELECT * 
          FROM words 
         WHERE LabelName = 'Cat' COLLATE NOCASE 
           AND LabelType = 'Noun_Felidae_Cougar_Puma_Lynx' 
         """, cls=WiktionaryItem )

    try:
        wd = next(rows)

    except StopIteration:
        raise Exception("Not found: CAT-FELIDAE")

    #
    ExplainationExamplesTxt = get_sentences_with_label( wd.Description, wd.LabelName )
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

    return preference


def operation_pref_wikidata():
    for wd in DBRead( DBWord, sql=" SELECT * FROM words WHERE FromWD is not NULL ", cls=WordItem ):

        ExplainationExamplesTxt = get_sentences_with_label( wd.Description, wd.LabelName )
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

        preference_base = get_preference( 'CAT-FELIDAE' )

        if preference is None:
            continue

        #
        if preference_base == 0:
            x = preference / preference_base / 2

            if x <= 0:
                LabelNamePreference = 0
            else:
                LabelNamePreference = 1

            DBExecute( DBWiktionary, """
                UPDATE words 
                   SET LabelNamePreference = ? 
                 WHERE PK = ?
                 """, LabelNamePreference, wd.PK )


def operation_pref_wiktionary():
    ...



def operation_pref():
    operation_pref_wikidata()
