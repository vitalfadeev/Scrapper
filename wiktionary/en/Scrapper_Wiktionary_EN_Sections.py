from wiktionary.Scrapper_Wiktionary_ValuableSections import VALUABLE_SECTIONS as ws
from wiktionary.Scrapper_Wiktionary_WordTypes import WORD_TYPES as wt


LANG_SECTIONS = {
    'english': [
        'english',
        'en',
    ],
}


PART_OF_SPEECH_SECTIONS = {
    # common
    wt.NOUN: [
        'noun',
        'noun 1',
        'noun 2',
        'noun 3',
    ],
    wt.ADJECTIVE: [
        'adjective',
    ],
    wt.VERB: [
        'verb',
        'verb 1',
        'verb 2',
        'verb 3',
    ],
    wt.ADVERB: [
        'adverb',
    ],
    wt.PREDICATIVE: [
        'predicative',
    ],
    wt.CONJUNCTION: [
        'conjunction',
    ],
    wt.PREPOSITION: [
        'preposition',
    ],
    wt.PRONOUN: [
        'pronoun',
        'prepositional pronoun',
    ],
    wt.INTERJECTION: [
        'interjection',
        'interjection 1',
        'interjection 2',
    ],
    wt.PARTICLE: [
        'particle',
        'particle 1',
        'particle 2',
    ],
    wt.ARTICLE: [
        'article',
    ],
    wt.NUMERAL: [
        'numeral',
    ],
    wt.ABBREV: [
        'abbreviations',
        'abbrev'
        'abbreviation',
    ],
    # rare
    wt.PREFIX: [
        'prefix',
    ],
    wt.PREVERB: [
        'preverb',
    ],
    wt.PARTICIPLE: [
        'participle',
        'participles',
    ],
    wt.PROPERNOUN: [
        'proper noun',
        'proper noun 1',
        'proper noun 2',
    ],
    wt.ACRONYM: [
        'acronym',
    ],
    wt.AFFIX: [
        'affix',
    ],
    wt.CONTRACTION: [
        'contraction',
    ],
    wt.DETERMINER: [
        'determiner',
    ],
    wt.HYPHENATION: [
        'hyphenation',
    ],
    wt.INFIX: [
        'infix',
    ],
    wt.INTERFIX: [
        'interfix',
    ],
    wt.LETTER: [
        'letter',
    ],
    wt.NUMBER: [
        'number',
        'ordinal number',
    ],
    wt.PHRASE: [
        'phrase',
    ],
    wt.POSTPOSITION: [
        'postposition',
    ],
    wt.PREPOSITIONAL_PHRASE: [
        'prepositional phrase',
    ],
    wt.PUNCTUATION_MARK: [
        'punctuation mark',
    ],
    wt.ROOT: [
        'root',
        'root word',
    ],
    wt.SUFFIX: [
        'suffix',
    ],
    wt.SYMBOL: [
        'symbol',
    ],
}


VALUED_SECTIONS = {
    ws.ETYMOLOGY: [
        'etymology',
        'etimology',
        'etmology',
        'etymologie',
        'etymology',
        'etymology 1',
        'etymology 2',
        'etymology 3',
        'etymology 4',
        'etymology 5',
        'etymology 6',
        'etymology 7',
        'etymology 8',
        'etymology 9',
        'etymolology',
        'etyology',
        'etyomology 1',
    ],
    ws.ALTERNATIVE_FORMS: [
        'alternative forms',
        'alternate forms',
        'alternative form',
        'aternative forms',
    ],
    ws.ANTONYMS: [
        'antonym',
        'antonyms',
    ],
    ws.DECLENSION: [
        'declension',
        'declension (fem.)',
        'declension (masc.)',
        'declension (neut.)',
        'declension 1',
        'declension 2',
    ],
    ws.SYNONYMS: [
        'synonym',
        'synonyms',
    ],
    ws.SEE_ALSO: [
        'see also',
        'ser also',
    ],
    ws.RELATED_TERMS: [
        'related terms',
        'relative',
        'relational',
    ],
    ws.PRONUNCIAITON: [
        'pronunciation',
        'pronunciation 1',
        'pronunciation 1.1',
        'pronunciation 1.2',
        'pronunciation 2',
        'pronunciation 3',
        'pronunciation 4',
    ],
    ws.ANAGRAMS: [
        'anagrams',
    ],
    ws.BIBLIOGRAPHY: [
        'bibliography'
    ],
    ws.BORROWINGS: [
        'borrowed terms',
        'borrowings',
    ],
    ws.CLASSIFIER: [
        'classifier',
    ],
    ws.COMPOUNDS: [
        'compounds',
        'compounds (extra long)',
    ],
    ws.CONJUGATION: [
        'conjugation',
        'conjugation 1',
        'conjugation 2',
    ],
    ws.COORDINATE_TERMS: [
        'coordinate terms',
    ],
    ws.DEFINITIONS: [
        'definitions',
    ],
    ws.DERIVED_COMPOUND_VERBS: [
        'derived compound verbs',
    ],
    ws.DERIVED_TERMS: [
        'derived terms',
        'derived terms / hyponyms',
    ],
    ws.DESCENDANTS: [
        'descendants',
    ],
    ws.EXPRESSIONS: [
        'expressions',
    ],
    ws.EXTERNAL_LINKS: [
        'external links',
    ],
    ws.FEMININE_DECLENSION: [
        'feminine declension',
    ],
    ws.HOLONYMS: [
        'holonyms',
    ],
    ws.HOMOPHONES: [
        'homophones',
    ],
    ws.HYPERNYMS: [
        'hypernyms',
    ],
    ws.HYPONYMS: [
        'hyponyms',
    ],
    ws.IDIOMS: [
        'idiom',
        'idioms',
    ],
    ws.INFLECTION: [
        'inflection',
    ],
    ws.INITIALISM: [
        'initialism',
    ],
    ws.MASCULINE_DECLENSION: [
        'masculine declension',
    ],
    ws.MERONYMS: [
        'meronyms',
    ],
    ws.MUTATION: [
        'mutation',
    ],
    ws.NOTES: [
        'notes',
    ],
    ws.PARONYMS: [
        'paronyms',
    ],
    ws.PHRASES: [
        'phrases',
    ],
    ws.PRODUCTION: [
        'production',
    ],
    ws.PROVERBS: [
        'proverbs',
    ],
    ws.PUNCTUATION: [
        'punctuation',
    ],
    ws.QUOTATIONS: [
        'quotations',
    ],
    ws.REFERENCES: [
        'references',
    ],
    ws.RESOURCES: [
        'resources',
    ],
    ws.STATISTICS: [
        'statistics',
    ],
    ws.TRANSLATIONS: [
        'translation',
        'translations',
    ],
    ws.TROPONYMS: [
        'troponyms',
    ],
    ws.USAGE_NOTES: [
        'usage notes',
    ],
}


# LANG_SECTIONS optimization
# INDEX: {'english':'english', 'en':'english'}
LANG_SECTIONS_INDEX = {}
for name, aliases in LANG_SECTIONS.items():
    LANG_SECTIONS_INDEX.update( dict.fromkeys(aliases, name) )

# PART_OF_SPEECH_SECTIONS optimization
# INDEX: {'noun':'noun', 'noun 1':'noun', 'noun 2':'noun'}
PART_OF_SPEECH_SECTIONS_INDEX = {}
for name, aliases in PART_OF_SPEECH_SECTIONS.items():
    PART_OF_SPEECH_SECTIONS_INDEX.update( dict.fromkeys(aliases, name) )

# VALUED_SECTIONS optimization
# INDEX: {'synonyms':'synonyms', 'syn':'synonyms', 'sinonyms':'synonyms'}
VALUED_SECTIONS_INDEX = {}
for name, aliases in VALUED_SECTIONS.items():
    VALUED_SECTIONS_INDEX.update( dict.fromkeys(aliases, name) )


"""
def normalize(lexems):
    NORMALIZATION_INDEX = {}
    NORMALIZATION_INDEX.update(LANG_SECTIONS_INDEX)
    NORMALIZATION_INDEX.update(PART_OF_SPEECH_SECTIONS_INDEX)
    NORMALIZATION_INDEX.update(VALUED_SECTIONS_INDEX)

    for lexem in  lexems:
        try:
            if isinstance(lexem, Header):
                lexem.raw_name = lexem.name
                lexem.name = NORMALIZATION_INDEX[lexem.name]
        except KeyError:
            pass

    return lexems
"""
