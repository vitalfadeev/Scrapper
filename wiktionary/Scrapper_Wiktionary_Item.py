#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from collections.abc import Iterable
from Scrapper_Helpers import remove_comments, extract_from_link, filterWodsProblems

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class WikictionaryItem:
    class Meta:
        DB_TABLE_NAME = "wiktionary"
        DB_INIT = """
            CREATE TABLE IF NOT EXISTS wiktionary (
                    PrimaryKey              VARCHAR(255) NOT NULL PRIMARY KEY,
                    SelfUrl                 VARCHAR(255),
                    LabelName               VARCHAR(255),
                    LabelType               VARCHAR(255),
                    LanguageCode            CHAR(2),
                    Type                    VARCHAR(255),
                    TypeLabelName           VARCHAR(255),
                    ExplainationRaw         TEXT,
                    ExplainationTxt         TEXT,
                    ExplainationExamplesRaw TEXT,
                    ExplainationExamplesTxt TEXT,
                    IsMale                  INTEGER NULL,
                    IsFeminine              INTEGER NULL,
                    IsNeutre                INTEGER NULL,
                    IsSingle                INTEGER NULL,
                    IsPlural                INTEGER NULL,
                    SingleVariant           VARCHAR(255) NULL,
                    PluralVariant           VARCHAR(255) NULL,
                    PopularityOfWord        INTEGER NULL,
                    MaleVariant             VARCHAR(255) NULL,
                    FemaleVariant           VARCHAR(255) NULL,
                    IsVerbPast              INTEGER NULL,
                    IsVerbPresent           INTEGER NULL,
                    IsVerbFutur             INTEGER NULL,
                    Conjugation             TEXT NULL,
                    Synonymy                TEXT NULL,
                    Antonymy                TEXT NULL,
                    Hypernymy               TEXT NULL,
                    Hyponymy                TEXT NULL,
                    Meronymy                TEXT NULL,
                    Holonymy                TEXT NULL,
                    Troponymy               TEXT NULL,
                    Otherwise               TEXT NULL,
                    AlternativeFormsOther   TEXT NULL,
                    RelatedTerms            TEXT NULL,
                    Coordinate              TEXT NULL,
                    Translation_EN          TEXT NULL,
                    Translation_FR          TEXT NULL,
                    Translation_DE          TEXT NULL,
                    Translation_IT          TEXT NULL,
                    Translation_ES          TEXT NULL,
                    Translation_RU          TEXT NULL,
                    Translation_PT          TEXT NULL,
                    IndexinPage				INTEGER NULL,
                    IndexinToc 				VARCHAR(255) NULL,
                    IndexPartOfSpeech		VARCHAR(255) NULL,
                    TranslationsBySentence  TEXT NULL,
                    TranslationSentence     TEXT NULL,
                    TranslationsByLang      TEXT NULL,
                    TranslationsPairs       TEXT NULL,
                    DescriptionWiktionaryLinks TEXT NULL,
                    DescriptionWikipediaLinks  TEXT NULL,
                    Labels                  TEXT NULL,
                    Categories              TEXT NULL,
                    Cognates                TEXT NULL,
                    Mentions                TEXT NULL,
                    VerbConjugaisonAdded    INTEGER NULL,
                    SenseRaw                TEXT NULL,
                    Sense                   TEXT NULL,
                    SenseFromSynonyms       TEXT NULL,
                    SenseFromTranslations   TEXT NULL,
                    SeeAlso                 TEXT NULL,
                    Accent                  TEXT NULL,
                    Qualifier               TEXT NULL,
                    ExternalLinks           TEXT NULL
            );
            
            -- CREATE INDEX IF NOT EXISTS  LanguageCode ON wiktionary (LanguageCode);
        """

    def __init__(self):
        self.PrimaryKey                 = ""
        self.SelfUrl                    = ""
        self.LabelName                  = ""  #
        self.LabelType                  = ""  #
        self.LanguageCode               = ""  # (EN,FR,…)
        self.Type                       = ""  #                        = noun,verb… see = WORD_TYPES
        self.TypeLabelName              = ""  # chatt for verb of chat
        self.ExplainationRaw            = ""  #
        self.ExplainationTxt            = ""  #
        self.ExplainationExamplesRaw    = ""
        self.ExplainationExamplesTxt    = ""
        self.IsMale                     = bool
        self.IsFeminine                 = bool  # ""
        self.IsNeutre                   = bool  # ""
        self.IsSingle                   = bool
        self.IsPlural                   = bool
        self.SingleVariant              = ""  # ""
        self.PluralVariant              = ""  # ""
        self.PopularityOfWord           = 0
        self.MaleVariant                = ""  # ""
        self.FemaleVariant              = ""  # ""
        self.IsVerbPast                 = bool
        self.IsVerbPresent              = bool
        self.IsVerbFutur                = bool
        self.Conjugation                = []
        self.Synonymy                   = []
        self.Antonymy                   = []
        self.Hypernymy                  = []
        self.Hyponymy                   = []
        self.Meronymy                   = []
        self.Holonymy                   = []
        self.Troponymy                  = []
        self.Otherwise                  = []
        self.AlternativeFormsOther      = []
        self.RelatedTerms               = []
        self.Coordinate                 = []
        self.Translation_EN             = []
        self.Translation_FR             = []
        self.Translation_DE             = []
        self.Translation_IT             = []
        self.Translation_ES             = []
        self.Translation_RU             = []
        self.Translation_PT             = []
        self.IndexinPage                = 0
        self.IndexinToc                 = "" # ""
        self.IndexPartOfSpeech          = "" # ""
        self.TranslationsBySentence     = {}
        self.TranslationSentence        = {}
        self.TranslationsByLang         = {}
        self.TranslationsPairs          = []
        self.DescriptionWiktionaryLinks = []
        self.DescriptionWikipediaLinks  = []
        self.Labels                     = []
        self.Categories                 = []
        self.Cognates                   = {}
        self.Mentions                   = {}
        self.VerbConjugaisonAdded       = None
        self.SenseRaw                   = ""
        self.Sense                      = ""
        self.SenseFromSynonyms          = ""
        self.SenseFromTranslations      = ""
        self.SeeAlso                    = []
        self.Accent                     = []
        self.Qualifier                  = []
        self.ExternalLinks              = []


    def merge( self, item: "WikictionaryItem"):
        for name in filter( lambda s: s[0].isupper(), vars(self) ):
            store = getattr( self, name )
            value = getattr( item, name )

            if value is not None:
                if isinstance( store, list ):
                    store.extend( value )
                elif isinstance( store, dict ):
                    store.update( value )
                elif isinstance( store, bool ) or store is bool:
                    if value is True:
                        setattr( self, name, True )
                elif isinstance( store, str ) or store is str:
                    pass
                elif isinstance( store, int ) or store is int:
                    pass
                # elif isinstance( store, float ):
                #     if value:
                #         setattr( self, name, value )
                else:
                    raise Exception( "unsupported: " + str( type( store ) ) )


    def add_explaniation(self, raw, txt):
        self.ExplainationRaw = raw
        self.ExplainationTxt = txt

    
    def add_conjugation(self, lang, term):
        term = filterWodsProblems(term, log)
        if term:
            if term != self.LabelName:
                if self.Conjugation is None:
                    self.Conjugation = [ term ]
                else:
                    if term not in self.Conjugation:
                        self.Conjugation.append( term )
    

    def add_synonym(self, lang, term):
        term = filterWodsProblems(term, log)
        if term:
            if term != self.LabelName:
                if self.Synonymy is None:
                    self.Synonymy = [ term ]
                else:
                    if term not in self.Synonymy:
                        self.Synonymy.append( term )
    

    def add_antonym(self, lang, term):
        term = filterWodsProblems(term, log)
        if term:
            if term != self.LabelName:
                if self.Antonymy is None:
                    self.Antonymy = [ term ]
                else:
                    if term not in self.Antonymy:
                        self.Antonymy.append( term )

    
    def add_hypernym(self, lang, term):
        term = filterWodsProblems(term, log)
        if term:
            if term != self.LabelName:
                if self.Hypernymy is None:
                    self.Hypernymy = [ term ]
                else:
                    if term not in self.Hypernymy:
                        self.Hypernymy.append( term )
    

    def add_hyponym(self, lang, term):
        term = filterWodsProblems(term, log)
        if term:
            if term != self.LabelName:
                if self.Hyponymy is None:
                    self.Hyponymy = [ term ]
                else:
                    if term not in self.Hyponymy:
                        self.Hyponymy.append( term )
    

    def add_meronym(self, lang, term):
        term = filterWodsProblems(term, log)
        if term:
            if term != self.LabelName:
                if self.Meronymy  is None:
                    self.Meronymy = [ term ]
                else:
                    if term not in self.Meronymy:
                        self.Meronymy.append( term )
    

    def add_holonym(self, lang, term):
        term = filterWodsProblems(term, log)
        if term:
            if term != self.LabelName:
                if self.Holonymy  is None:
                    self.Holonymy = [ term ]
                else:
                    if term not in self.Holonymy:
                        self.Holonymy.append( term )
    

    def add_troponym(self, lang, term):
        term = filterWodsProblems(term, log)
        if term:
            if term != self.LabelName:
                if self.Troponymy is None:
                    self.Troponymy = [ term ]
                else:
                    if term not in self.Troponymy:
                        self.Troponymy.append( term )
    

    def add_alternative_form(self, lang, term):
        term = filterWodsProblems(term, log)
        if term:
            if term != self.LabelName:
                if self.AlternativeFormsOther is None:
                    self.AlternativeFormsOther = [ term ]
                else:
                    if term not in self.AlternativeFormsOther:
                        self.AlternativeFormsOther.append( term )
    

    def add_related(self, lang, term):
        term = filterWodsProblems(term, log)
        if term:
            if term != self.LabelName:
                if self.RelatedTerms is None:
                    self.RelatedTerms = [ term ]
                else:
                    if term not in self.RelatedTerms:
                        self.RelatedTerms.append( term )
    

    def add_coordinate(self, lang, term):
        term = filterWodsProblems(term, log)
        if term:
            if term != self.LabelName:
                if self.Coordinate is None:
                    self.Coordinate = [ term ]
                else:
                    if term not in self.Coordinate:
                        self.Coordinate.append( term )

    
    def add_translation(self, lang, term):
        # validate
        if term is None:
            # skip None
            return
            
        term = remove_comments(term)
        term = extract_from_link(term)
        term = term.strip()
        
        if not term:
            # skip blank
            # skip empty
            return

        # prepare
        storages = {
            "en": "Translation_EN",
            "fr": "Translation_FR",
            "de": "Translation_DE",
            "it": "Translation_IT",
            "es": "Translation_ES",
            "ru": "Translation_RU",
            "pt": "Translation_PT",
            #"cn": "Translation_CN",
            #"ja": "Translation_JA"
        }

        # check lang
        if lang not in storages:
            # not supported language
            log.debug("unsupported language: " + str(lang))
            return

        # filter
        term = filterWodsProblems(term, log)

        # storage
        storage_name = storages.get(lang, None)

        # init storage
        storage = getattr(self, storage_name)
        if storage is None:
            # init
            storage = []
            setattr(self, storage_name, storage)

        # append
        if term is None:
            pass
            
        elif isinstance(term, str):
            # one
            if term not in storage:
                storage.append( term )

        elif isinstance(term, Iterable):
            # [list] | (tuple)
            for trm in term:
                if term not in storage:
                    storage.append( term )

        else:
            log.error("unsupported type: %s", type(term))
            # assert 0, "unsupported type"

            
    def clone(self):
        clone = WikictionaryItem()
        
        for name in self.get_fields():
            value = getattr(self, name)
            if isinstance(value, list):
                cloned_value = value.copy()
            else:
                cloned_value = value
            setattr(clone, name, cloned_value)
        
        return clone


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
        return "WikictionaryItem(" + self.LabelName + ")"


