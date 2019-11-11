#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

log = logging.getLogger(__name__)

class WiktionaryItem:
    class Meta:
        DB_TABLE_NAME = "wiktionary"
        DB_INIT = """
            CREATE TABLE IF NOT EXISTS wiktionary (
                    PrimaryKey                  VARCHAR(255) NOT NULL PRIMARY KEY,
                    IndexinPage				    INTEGER NULL,
                    IndexPartOfSpeech		    VARCHAR(255) NULL,
                    IndexinToc 				    VARCHAR(255) NULL,
                    SelfUrl                     VARCHAR(255),
                    LabelName                   VARCHAR(255),
                    LabelType                   VARCHAR(255),
                    LanguageCode                CHAR(2),
                    Type                        VARCHAR(255),
                    TypeLabelName               VARCHAR(255),
                    ExplainationRaw             TEXT,
                    ExplainationTxt             TEXT,
                    ExplainationExamplesRaw     TEXT,
                    ExplainationExamplesTxt     TEXT,
                    DescriptionTxt              TEXT,
                    IsMale                      INTEGER NULL,
                    IsFeminine                  INTEGER NULL,
                    IsNeutre                    INTEGER NULL,
                    IsSingle                    INTEGER NULL,
                    IsPlural                    INTEGER NULL,
                    SingleVariant               VARCHAR(255) NULL,
                    PluralVariant               VARCHAR(255) NULL,
                    PopularityOfWord            INTEGER NULL,
                    MaleVariant                 VARCHAR(255) NULL,
                    FemaleVariant               VARCHAR(255) NULL,
                    IsVerbPast                  INTEGER NULL,
                    IsVerbPresent               INTEGER NULL,
                    IsVerbFutur                 INTEGER NULL,
                    Conjugation                 TEXT NULL,
                    Synonymy                    TEXT NULL,
                    Antonymy                    TEXT NULL,
                    Hypernymy                   TEXT NULL,
                    Hyponymy                    TEXT NULL,
                    Meronymy                    TEXT NULL,
                    Holonymy                    TEXT NULL,
                    Troponymy                   TEXT NULL,
                    Otherwise                   TEXT NULL,
                    AlternativeFormsOther       TEXT NULL,
                    RelatedTerms                TEXT NULL,
                    DerivedTerms                TEXT NULL,
                    Coordinate                  TEXT NULL,
                    Translation_EN              TEXT NULL,
                    Translation_FR              TEXT NULL,
                    Translation_DE              TEXT NULL,
                    Translation_IT              TEXT NULL,
                    Translation_ES              TEXT NULL,
                    Translation_RU              TEXT NULL,
                    Translation_PT              TEXT NULL,
                    TranslationsBySentence      TEXT NULL,
                    TranslationSentence         TEXT NULL,
                    TranslationsByLang          TEXT NULL,
                    TranslationsPairs           TEXT NULL,
                    Labels                      TEXT NULL,
                    Categories                  TEXT NULL,
                    Cognates                    TEXT NULL,
                    Mentions                    TEXT NULL,
                    VerbConjugaisonAdded        INTEGER NULL,
                    Senses                      TEXT NULL,
                    SeeAlsoWiktionaryLinks      TEXT NULL,
                    SeeAlsoWikipediaLinks       TEXT NULL,
                    Accent                      TEXT NULL,
                    Qualifier                   TEXT NULL,
                    DescriptionWikipediaLinks   TEXT NULL,
                    DescriptionWiktionaryLinks  TEXT NULL,
                    
                    LabelNamePreference    		INTEGER, 
                    Operation_Merging    		INTEGER, 
                    Operation_Pref    	    	INTEGER 
            );
            
            -- CREATE INDEX IF NOT EXISTS  LanguageCode ON wiktionary (LanguageCode);
        """

    def __init__(self):
        self.PrimaryKey                  = ""
        self.SelfUrl                     = ""
        self.LabelName                   = ""  #
        self.LabelType                   = ""  #
        self.LanguageCode                = ""  # (EN,FR,…)
        self.Type                        = ""  #                        = noun,verb… see = WORD_TYPES
        self.TypeLabelName               = ""  # chatt for verb of chat
        self.ExplainationRaw             = ""  #
        self.ExplainationTxt             = ""  #
        self.ExplainationExamplesRaw     = ""
        self.ExplainationExamplesTxt     = ""
        self.DescriptionTxt              = ""
        self.IsMale                      = bool
        self.IsFeminine                  = bool  # ""
        self.IsNeutre                    = bool  # ""
        self.IsSingle                    = bool
        self.IsPlural                    = bool
        self.SingleVariant               = ""  # ""
        self.PluralVariant               = ""  # ""
        self.PopularityOfWord            = 0
        self.MaleVariant                 = ""  # ""
        self.FemaleVariant               = ""  # ""
        self.IsVerbPast                  = bool
        self.IsVerbPresent               = bool
        self.IsVerbFutur                 = bool
        self.Conjugation                 = []
        self.Synonymy                    = []
        self.Antonymy                    = []
        self.Hypernymy                   = []
        self.Hyponymy                    = []
        self.Meronymy                    = []
        self.Holonymy                    = []
        self.Troponymy                   = []
        self.Otherwise                   = []
        self.AlternativeFormsOther       = []
        self.RelatedTerms                = []
        self.DerivedTerms                = []
        self.Coordinate                  = []
        self.Translation_EN              = []
        self.Translation_FR              = []
        self.Translation_DE              = []
        self.Translation_IT              = []
        self.Translation_ES              = []
        self.Translation_RU              = []
        self.Translation_PT              = []
        self.IndexinPage                 = 0
        self.IndexinToc                  = "" # ""
        self.IndexPartOfSpeech           = "" # ""
        self.TranslationsBySentence      = {}
        self.TranslationSentence         = {}
        self.TranslationsByLang          = {}
        self.TranslationsPairs           = []
        self.DescriptionWiktionaryLinks  = []
        self.DescriptionWikipediaLinks   = []
        self.Labels                      = []
        self.Categories                  = []
        self.Cognates                    = {}
        self.Mentions                    = {}
        self.VerbConjugaisonAdded        = None
        self.Senses                      = {}
        self.SeeAlsoWiktionaryLinks      = []
        self.SeeAlsoWikipediaLinks       = []
        self.Accent                      = []
        self.Qualifier                   = []
        self.DescriptionWikipediaLinks   = []
        self.DescriptionWiktionaryLinks  = []

        self.LabelNamePreference         = 0
        self.Operation_Merging           = 0
        self.Operation_Pref              = 0


    def dump(self, print_header=False):
        """ Beauty logging tool """
        attrs = [
            "LabelName",
            "LabelType",
            "LanguageCode",
            "Type",
            "ExplainationRaw",
            "ExplainationTxt",
            # "ExplainationExamplesRaw",
            # "ExplainationExamplesTxt",
            "IsMale",
            "IsFeminine",
            "IsNeutre",
            "IsSingle",
            "IsPlural",
            "SingleVariant",
            "PluralVariant",
            "MaleVariant",
            "FemaleVariant",
            "IsVerbPast",
            "IsVerbPresent",
            "IsVerbFutur",
            "Conjugation",
            "Synonymy",
            "Antonymy",
            "Hypernymy",
            "Hyponymy",
            "Meronymy",
            "Holonymy",
            "Troponymy",
            "Otherwise",
            "AlternativeFormsOther",
            "RelatedTerms",
            "Coordinate",
            "Translation_EN",
            "Translation_FR",
            "Translation_DE",
            "Translation_IT",
            "Translation_ES",
            "Translation_RU",
            "Translation_PT",
            "TranslationsBySentence",
            "TranslationsByLang",
            "DescriptionWiktionaryLinks",
            "DescriptionWikipediaLinks"
        ]
        header = []
        if print_header:
            for a in attrs:
                s = ""
                for c in a:
                    if c.isalpha() and c == c.upper():
                        s += c
                        if len(s) >= 1:
                            break
                header.append(s.rjust(2))
            log.info(" ".join(header))

        row = []
        for a in attrs:
            value = getattr(self, a)
            if value and isinstance(value, (tuple, list)):
                s = str( len( value ) )
            else:
                if value is bool:
                    s = '-'
                elif value:
                    s = '*'
                else:
                    s = '-'
            row.append(s.rjust(2))
        log.info(" ".join(row) + " " + self.PrimaryKey)


    def dumps(self, print_header=False):
        """ Beauty logging tool """
        attrs = [
            "LabelType",
            "ExplainationRaw",
            "ExplainationTxt",
            "ExplainationExamplesRaw",
            "ExplainationExamplesTxt",
            "IsMale",
            "IsFeminine",
            "IsNeutre",
            "IsSingle",
            "IsPlural",
            "SingleVariant",
            "PluralVariant",
            "MaleVariant",
            "FemaleVariant",
            "IsVerbPast",
            "IsVerbPresent",
            "IsVerbFutur",
            "Conjugation",
            "Synonymy",
            "Antonymy",
            "Hypernymy",
            "Hyponymy",
            "Meronymy",
            "Holonymy",
            "Troponymy",
            "Otherwise",
            "AlternativeFormsOther",
            "RelatedTerms",
            "Coordinate",
            "Translation_EN",
            "Translation_FR",
            "Translation_DE",
            "Translation_IT",
            "Translation_ES",
            "Translation_RU",
            "Translation_PT",
        ]

        s = ""

        header = ["   "]
        if print_header:
            for a in attrs:
                s = ""
                for c in a:
                    if c.isalpha() and c == c.upper():
                        s += c
                        if len(s) >= 1:
                            break
                header.append(s.rjust(2))
            #log.info(" ".join(header))
            s = " ".join(header)
            return s

        row = [str(self.IndexinPage).rjust(3)]
        for a in attrs:
            value = getattr(self, a)
            if value and isinstance(value, (tuple, list)):
                s = str(len(value))
            else:
                if value:
                    s = '*'
                else:
                    s = '-'
            row.append(s.rjust(2))
        #log.info(" ".join(row) + " " + self.PrimaryKey)
        s = " ".join(row) + " " + self.PrimaryKey
        #s = " ".join(row)

        return s


    def __repr__(self):
        return "WikictionaryItem(" + self.LabelName + ': ' + self.PrimaryKey + ")"


