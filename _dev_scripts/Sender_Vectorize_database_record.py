import requests
from pprint import pprint as pp
import json

url = "http://lviv.ixioo.com:8030/Vectorize_database_record"

database_record = {'LabelType': 'Noun-EXTENSION-LIST', 'AlternativeFormsOther': None, 'Antonymy': None, 'Conjugation': None, 'Coordinate': None, 'ExplainationExamplesRaw': None, 'ExplainationExamplesTxt': None, 'ExplainationRaw': '# {{lb|en|by extension}} Any work that has a [[list]] of [[material]] organized alphabetically; e.g., [[biographic]]al dictionary, [[encyclopedic]] dictionary.', 'ExplainationTxt': 'Any work that has a list of material organized alphabetically; e.g., biographical dictionary, encyclopedic dictionary.', 'Holonymy': None, 'Hypernymy': None, 'Hyponymy': None, 'IsSingle': 1, 'LabelName': 'dictionary', 'LanguageCode': 'en', 'Meronymy': None, 'Otherwise': None, 'PluralVariant': 'dictionaries', 'PrimaryKey': 'en§dictionary§Noun-EXTENSION-LIST§1§84', 'RelatedTerms': '[\n    "diction"\n]', 'SelfUrl': 'https://en.wiktionary.org/wiki/dictionary', 'Synonymy': '[\n    "Thesaurus:dictionary"\n]', 'Translation_DE': '[\n    "assoziatives Datenfeld",\n    "Wörterbuch",\n    "Diktionär"\n]', 'Translation_EN': None, 'Translation_ES': '[\n    "diccionario"\n]', 'Translation_FR': '[\n    "table d\'association",\n    "dictionnaire",\n    "dico",\n    "tableau associatif"\n]', 'Translation_IT': '[\n    "dizionario",\n    "vocabolario"\n]', 'Translation_PT': '[\n    "array associativo",\n    "dicionário"\n]', 'Translation_RU': '[\n    "слова́рь"\n]', 'Troponymy': None, 'Type': 'noun', 'TypeLabelName': None, 'IsPlural': None, 'SingleVariant': None, 'IsFeminine': None, 'IsMale': None, 'MaleVariant': None, 'IsVerbPast': None, 'IsVerbPresent': None, 'FemaleVariant': None, 'IsVerbFutur': None, 'PopularityOfWord': None}
data = {
    'database_record': database_record
}
r = requests.post(url, json=data)
print('Sent a request.')
pp(json.loads(r.text))

'''
    For request you send dictionary - data
    data contains 1 key:
    ~ 'database_record' - one row from database (dicitonary)

    Function returns string representation of a dictionary
    this dictionary will have the same keys as 'database_record' dictionary, with values vectorized
    using json.loads() you can transform it back to a dictionary
'''