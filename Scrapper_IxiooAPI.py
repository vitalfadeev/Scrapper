from functools import lru_cache

import requests
import json
import logging
from Scrapper_Helpers import retry

log = logging.getLogger(__name__)

"""
    This module will make a post request to the URL, as an argument it will pass a json file (dictionary)
    which will contain two keys: 'explanations' and 'translations', value of each will be a list of strings.

    * 'explanations' list will contain all the explanations of the word from DB
    * 'explanations' list will contain all the explanations of the word from DB
    * 'explanations' list will contain all the explanations of the word from DB

    * 'translations' list will contain all the {explanations of translations} to the word

    In result response will contain a json file (dictionary) which will have one key - 'result'
    the value of 'result' will be a list, each element of the list is another list, containing pairs of strings
    (Match_List_PKS_With_Lists_Of_PKS will try to match each explanation to its best translation explanation)
    first element will be explanation and second - corresponding explanation of translation

    If our function didn't find a matching explanation of translation then it will return a list:
    first element will be explanation and second - null

"""

DOMAIN = 'http://lviv.ixioo.com:8030'

@lru_cache( maxsize=32 )
@retry((requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.HTTPError), tries=5, delay=1)
def Match_List_PKS_With_Lists_Of_PKS(explanations: tuple, translation_sentences: tuple) -> list:
    """
    Send explanation sentences list and translation sentences list to the PKS_Matcher and return pairs.

    Each pair is [explanations, translation].

    if matched: [explanations, translation], it not matched: [explanations, None]

    Args:
        explanations (tuple):           Explanation sentences
        translation_sentences (tuple):  Tranlation sentences

    Returns:
        (list) Pairs: [ [Explanation sentences, Tranlation sentences], [...] ]. If matched: [e, s], if not matched: [e, None]

    ::

        matches = Scrapper_IxiooAPI.Match_List_PKS_With_Lists_Of_PKS( tuple(explanation_senses), tuple(section_senses) )

    """
    url = DOMAIN + '/Match_List_PKS_With_Lists_Of_PKS'
    data = {
        'explanations': explanations,
        'translations': translation_sentences,
    }

    #
    log.debug( "    Request to: %s", url )
    response = requests.post(url, json=data, timeout=(11, 33))

    if response.status_code == 200:
        try:
            result = json.loads( response.content, encoding='UTF-8' )
            pairs = result['result']
            return pairs

        except json.decoder.JSONDecodeError as e:
            log.error( '  explanations: %s', explanations )
            log.error( '  translation_sentences: %s', translation_sentences )
            log.error( '  response.text: %s', response.text )
            raise e

    else:
        log.error( "  %s", response.status_code )
        log.error( "  %s", response.text )
        return None


@retry((requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.HTTPError), tries=5, delay=1)
def Vectorize_database_record( database_record: dict ) -> list:
    url = DOMAIN + '/Vectorize_database_record'

    # database_record = { 'LabelType': 'Noun-EXTENSION-LIST',
    #                     'AlternativeFormsOther': None,
    #                     'Antonymy': None,
    #                     'Conjugation': None,
    #                     'Coordinate': None,
    #                     'ExplainationExamplesRaw': None,
    #                     'ExplainationExamplesTxt': None,
    #                     'ExplainationRaw': '# {{lb|en|by extension}} Any work that has a [[list]] of [[material]] organized alphabetically; e.g., [[biographic]]al dictionary, [[encyclopedic]] dictionary.',
    #                     'ExplainationTxt': 'Any work that has a list of material organized alphabetically; e.g., biographical dictionary, encyclopedic dictionary.',
    #                     'Holonymy': None,
    #                     'Hypernymy': None,
    #                     'Hyponymy': None,
    #                     'IsSingle': 1,
    #                     'LabelName': 'dictionary',
    #                     'LanguageCode': 'en',
    #                     'Meronymy': None,
    #                     'Otherwise': None,
    #                     'PluralVariant': 'dictionaries',
    #                     'PrimaryKey': 'en§dictionary§Noun-EXTENSION-LIST§1§84', 'RelatedTerms': '[\n    "diction"\n]',
    #                     'SelfUrl': 'https://en.wiktionary.org/wiki/dictionary',
    #                     'Synonymy': '[\n    "Thesaurus:dictionary"\n]',
    #                     'Translation_DE': '[\n    "assoziatives Datenfeld",\n    "Wörterbuch",\n    "Diktionär"\n]',
    #                     'Translation_EN': None,
    #                     'Translation_ES': '[\n    "diccionario"\n]',
    #                     'Translation_FR': '[\n    "table d\'association",\n    "dictionnaire",\n    "dico",\n    "tableau associatif"\n]',
    #                     'Translation_IT': '[\n    "dizionario",\n    "vocabolario"\n]',
    #                     'Translation_PT': '[\n    "array associativo",\n    "dicionário"\n]',
    #                     'Translation_RU': '[\n    "слова́рь"\n]',
    #                     'Troponymy': None, 'Type': 'noun',
    #                     'TypeLabelName': None,
    #                     'IsPlural': None,
    #                     'SingleVariant': None,
    #                     'IsFeminine': None,
    #                     'IsMale': None,
    #                     'MaleVariant': None,
    #                     'IsVerbPast': None,
    #                     'IsVerbPresent': None,
    #                     'FemaleVariant': None,
    #                     'IsVerbFutur': None,
    #                     'PopularityOfWord': None }
    data = {
        'database_record':database_record,

    }

    #
    log.debug( "    Request to: %s", url )
    response = requests.post(url, json=data, timeout=(11, 33))

    if response.status_code == 200:
        try:
            result = json.loads( response.content, encoding='UTF-8' )
            return result # database record

        except json.decoder.JSONDecodeError as e:
            log.error( '  database_record: %s', database_record )
            log.error( '  response.text: %s', response.text )
            raise e

    else:
        log.error( "  %s", response.status_code )
        log.error( "  %s", response.text )
        return None

