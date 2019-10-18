from functools import lru_cache

import requests
import json

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
def Match_List_PKS_With_Lists_Of_PKS(explanations: tuple, translation_sentences: tuple) -> list:
    url = DOMAIN + '/Match_List_PKS_With_Lists_Of_PKS'
    data = {
        'explanations': explanations,
        'translations': translation_sentences,
    }

    response = requests.post(url, json=data, timeout=(11, 33))

    if response.status_code == 200:
        try:
            result = json.loads( response.content, encoding='UTF-8' )
            pairs = result['result']
            return pairs

        except json.decoder.JSONDecodeError as e:
            print( 'explanations:', explanations )
            print( 'translation_sentences:', translation_sentences )
            print( 'response.text:', response.text )
            raise e

    else:
        print( response.status_code )
        print( response.text )
        return None

