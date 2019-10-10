class WORD_TYPES:
    """ Word type of speech"""
    ROOT        = "root"  # also ===Proper noun=== {{en-proper noun}}
    NOUN        = "noun"  # also ===Proper noun=== {{en-proper noun}}
    VERB        = "verb"
    PROVERB     = "proverb"
    CONVERB     = "converb"
    ADJECTIVE   = "adjective"
    ADVERB      = "adverb"
    ADNOUN      = "adj_noun"
    PRONOUN     = "pronoun"
    PREPOSITION = "preposition"
    CONJUNCTION = "conjunction"
    DETERMINER  = "determiner"
    EXCLAMATION = "exclamation"
    INTERJECTION= "interjection"
    NUMERAL     = "num"
    PARTICLE    = "part"
    PARTICIPLE  = "participle"
    POSTPOSITION= "postp"
    CHARACTER   = "character"
    DIGIT       = "digit"
    ABBREV      = "abbrev"
    AFFIX       = "affix"
    INFIX       = "infix"
    NAME        = "name"
    PREFIX      = "prefix"
    INTERFIX    = "interfix"
    SUFFIX      = "suffix"
    SYMBOL      = "symbol"
    PUNCT       = "punct"
    NUMBER      = "number"
    PHRASE      = "phrase"
    ARTICLE     = "article"
    COUNTER     = "counter"
    CLITIC      = "clitic"
    CIRCUMFIX   = "circumfix"
    CIRCUMPOS   = "circumpos"
    CLASSIFIER  = "classifier"
    PREDICATIVE = "predicative"
    POSTP       = "postp"
    ORDINAL     = "ordinal"
    CLAUSE      = "clause"
    LETTER      = "letter"
    GERUND      = "gerund"
    CMD         = "cmd"
    COMBINING_FORM = "combining_form"
    ADJ_COMP    = "adj_comp"
    INTRO       = "intro"
    VOCATIVO    = "vocativo"
    PREVERB     = "preverb"
    PROPERNOUN  = "propernoun"
    ACRONYM     = "acronym"
    CONTRACTION = "contraction"
    HYPHENATION = 'hyphenation'
    PREPOSITIONAL_PHRASE = 'prepositional_phrase'
    PUNCTUATION_MARK = 'punctuation mark'

    def detect_type(self, s):
        for a in dir(self):
            if a.isupper():
                if getattr(self, a) == s.lower():
                    return getattr(self, a)

        return None  # not found type


    def get_names(self):
        """
        out:
            [
                (noun, noun),
                (Proper noun, noun),
                (section_title_lowercase, type),
            ]
        """
        names = []

        for a in dir(self):
            if a.isupper():
                names.append((getattr(self, a), getattr(self, a)))

        # fixes
        names.append(("Proper noun", self.NOUN))

        return names
