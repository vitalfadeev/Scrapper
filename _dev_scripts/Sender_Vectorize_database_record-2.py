import requests
from pprint import pprint as pp
import json

url = "http://lviv.ixioo.com:8030/Vectorize_database_record"

# database_record = {'LabelType': 'Noun-EXTENSION-LIST', 'AlternativeFormsOther': None, 'Antonymy': None, 'Conjugation': None, 'Coordinate': None, 'ExplainationExamplesRaw': None, 'ExplainationExamplesTxt': None, 'ExplainationRaw': '# {{lb|en|by extension}} Any work that has a [[list]] of [[material]] organized alphabetically; e.g., [[biographic]]al dictionary, [[encyclopedic]] dictionary.', 'ExplainationTxt': 'Any work that has a list of material organized alphabetically; e.g., biographical dictionary, encyclopedic dictionary.', 'Holonymy': None, 'Hypernymy': None, 'Hyponymy': None, 'IsSingle': 1, 'LabelName': 'dictionary', 'LanguageCode': 'en', 'Meronymy': None, 'Otherwise': None, 'PluralVariant': 'dictionaries', 'PrimaryKey': 'en§dictionary§Noun-EXTENSION-LIST§1§84', 'RelatedTerms': '[\n    "diction"\n]', 'SelfUrl': 'https://en.wiktionary.org/wiki/dictionary', 'Synonymy': '[\n    "Thesaurus:dictionary"\n]', 'Translation_DE': '[\n    "assoziatives Datenfeld",\n    "Wörterbuch",\n    "Diktionär"\n]', 'Translation_EN': None, 'Translation_ES': '[\n    "diccionario"\n]', 'Translation_FR': '[\n    "table d\'association",\n    "dictionnaire",\n    "dico",\n    "tableau associatif"\n]', 'Translation_IT': '[\n    "dizionario",\n    "vocabolario"\n]', 'Translation_PT': '[\n    "array associativo",\n    "dicionário"\n]', 'Translation_RU': '[\n    "слова́рь"\n]', 'Troponymy': None, 'Type': 'noun', 'TypeLabelName': None, 'IsPlural': None, 'SingleVariant': None, 'IsFeminine': None, 'IsMale': None, 'MaleVariant': None, 'IsVerbPast': None, 'IsVerbPresent': None, 'FemaleVariant': None, 'IsVerbFutur': None, 'PopularityOfWord': None}
database_record = {
    'PK': 'en§Belgium§Q31',
    'LabelName': 'Belgium',
    'LabelType': None,
    'LanguageCode': 'en',
    'Type': None,

    'IndexInPageWiktionary': None,
    'Description': 'federal constitutional monarchy in Western Europe',

    'DescriptionWikipediaLinks': None,
    'DescriptionWiktionaryLinks': None,

    'SelfUrlWikidata': 'https://www.wikidata.org/wiki/Q31',
    'SelfUrlWiktionary': None,
    'SelfUrlWikipedia': None,

    'Synonymy': None,
    'Antonymy': None,
    'Hypernymy': '["Q3624078", "Q43702", "Q6256", "Q20181813"]',
    'Hyponymy': None,

    'Holonymy': None,
    'Troponymy': None,
    'Meronymy': '["Q215669"]',
    'SeeAlso': None,
    'SeeAlsoWikipediaLinks': None,

    'RelatedTerms': None,
    'AlsoKnownAs': '["Kingdom of Belgium", "BEL", "be", "🇧🇪"]',
    'IsMale': None,

    'IsNeutre': None,
    'IsFeminine': None,
    'MaleVariant': None,
    'FemaleVariant': None,
    'IsSingle': None,

    'IsPlural': None,
    'SingleVariant': None,
    'PluralVariant': None,
    'IsVerbPast': None,
    'IsVerbPresent': None,

    'IsVerbFutur': None,
    'VerbTense': None,
    'Translation_EN': '["Belgium"]',
    'Translation_FR': '["Belgique"]',

    'Translation_DE': '["Belgien"]',
    'Translation_IT': '["Belgio"]',
    'Translation_ES': '["Bélgica"]',

    'Translation_RU': '["Бельгия"]',
    'Translation_PT': '["Bélgica"]',

    'Ext_Wikipedia_URL': "https://en.wikipedia.org/wiki/Belgium",
    'CountTotalOfWikipediaUrl': 260,

    'ExplainationExamplesTxt': None,
    'PopularityOfWord': None,

    'Instance_of': '["Q3624078", "Q43702", "Q6256", "Q20181813"]',
    'Subclass_of': None,
    'Part_of': '["Q215669"]',

    'WikipediaLinkCountTotal': '260',
    'ExplainationTxt': None,
    'Operation_Merging': None,
    'Operation_Wikipedia': None,

    'Operation_Vectorizer': None,
    'Operation_PropertiesInv': None,
    'Operation_VectSentences': None,
    'Operation_Pref': 1,

    'LabelNamePreference': 1,
    'FromWP': None,
    'FromWT': None,
    'FromWD': '["en§Belgium§Q31"]',
    'FromCJ': None,

    'MergedWith': None,
    'Description_Vect': None,
    'ExplainationTxt_Vect': None,
    'AlsoKnownAs_Vect': None,

    'Instance_of_Vect': None,
    'Subclass_of_Vect': None,
    'Part_of_Vect': None,
    'AlternativeFormsOther_Vect': None,

    'Synonymy_Vect': None,
    'Antonymy_Vect': None,
    'Hypernymy_Vect': None,
    'Hyponymy_Vect': None,
    'Meronymy_Vect': None,

    'RelatedTerms_Vect': None,
    'CoordinateTerms_Vect': None,
    'Otherwise_Vect': None,
    'Description_Inv': None,

    'ExplainationTxt_Inv': None,
    'AlsoKnownAs_Inv': None,
    'Instance_of_Inv': None,
    'Subclass_of_Inv': None,

    'Part_of_Inv': None,
    'AlternativeFormsOther_Inv': None,
    'Synonymy_Inv': None,
    'Antonymy_Inv': None,

    'Hypernymy_Inv': None,
    'Hyponymy_Inv': None,
    'Meronymy_Inv': None,
    'RelatedTerms_Inv': None,

    'CoordinateTerms_Inv': None,
    'Otherwise_Inv': None
}

data = {
    'database_record': database_record,
    # 'language_code': 'en',
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
