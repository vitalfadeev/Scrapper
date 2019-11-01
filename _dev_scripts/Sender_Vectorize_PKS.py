import requests
from pprint import pprint as pp
import json

url = 'http://lviv.ixioo.com:8030/Vectorize_PKS'
data = {
    'PKS': 'cat',
    'PKE_Context': 'en§cat§Noun-FELIDAE-Felidae§0§238',
    'default_language': 'en'
}
r = requests.post(url, json=data)
print('Sent a request.')
pp(json.loads(r.text))

'''
    For request you send a dictionary - data
    data contains 2 keys:
    ~ 'PKS' - a sentence to vectorize (string), or a single word (string)
    
    ~ 'PKE_Context' - a sentence for additional context (string), or PrimaryKeys (string) !!! OPTIONAL !!!
    Example: {'PKS': 'cat'}                                 ->  en§cat§Noun-FELIDAE-Felidae§0§238
             {'PKS': 'cat', 'PKE_Context': 'Linux command'} ->  en§cat§Noun-COMPUTING-UNIX§14§661
    Important to use when vectorizing synonyms, pass PK of a word when vectorizing it's synonyms, so the accuracy is higher
    
    ---ADDED NEW OPTIONAL KEY---
    ~ 'default_language' - language which you should use for searching in database (string -> 'en', 'ru', 'es',...)
    
    ---RULES---
    Now you have to pass at least one of optional parameters (or both), both of them cannot be None at the same time!
    - If in PKE_Context you passed PrimaryKey(s) you don't need to pass default_language
    - If in PKE_Context you passed PrimaryKey(s) AND you passed default_language, module will look for words
      which LanguageCode == default_language.
      Example:
              {'PKS': 'cat', 'PKE_Context': 'en§cat§Noun-FELIDAE-Felidae§0§238', 'default_language': 'ru'} -> {'result': 'ru§cat§_UNKNOWN_§§'}
              {'PKS': 'cat', 'PKE_Context': 'en§cat§Noun-FELIDAE-Felidae§0§238', 'default_language': 'en'} -> {'result': 'en§cat§Noun-FELIDAE-Felidae§0§238'}
      So priority is on the default_language
    - If in PKE_Context you passed a sentence - you have to pass default_language as well (this feature will be reworked later)
    
    Function returns string representation of a dictionary
    It contains one key - 'result', the value is a list of PrimaryKeys (strings) of each word from given sentence (or word)
    using json.loads() you can transform it back to a dictionary
'''