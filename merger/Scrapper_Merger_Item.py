class WordItem:
    class Meta:
        DB_TABLE_NAME = "words"
        DB_INIT = """
            CREATE TABLE IF NOT EXISTS words (
                PK                          VARCHAR(255) NOT NULL  PRIMARY KEY,
                LabelName                   VARCHAR(255) NULL COLLATE NOCASE,
                LabelType                   VARCHAR(255) NULL,
                LanguageCode                CHAR(2),        
                Type                        VARCHAR(255) NULL,
                IndexInPageWiktionary       INTEGER NULL,
                Description                 VARCHAR(255) NULL,
                DescriptionWikipediaLinks   TEXT NULL,
                DescriptionWiktionaryLinks  TEXT NULL,
                SelfUrlWikidata             VARCHAR(255) NULL,
                SelfUrlWiktionary           VARCHAR(255) NULL,
                SelfUrlWikipedia            VARCHAR(255) NULL,
                Synonymy                    TEXT NULL,
                Antonymy                    TEXT NULL,
                Hypernymy                   TEXT NULL,
                Hyponymy                    TEXT NULL,
                Holonymy                    TEXT NULL,
                Troponymy                   TEXT NULL,
                Meronymy                    TEXT NULL,
                SeeAlso                     TEXT NULL,
                SeeAlsoWikipediaLinks       TEXT NULL,
                RelatedTerms                TEXT NULL,
                AlsoKnownAs                 TEXT NULL,
                IsMale                      INTEGER NULL,
                IsNeutre                    INTEGER NULL,
                IsFeminine                  INTEGER NULL,
                MaleVariant                 VARCHAR(255) NULL,
                FemaleVariant               VARCHAR(255) NULL,
                IsSingle                    INTEGER NULL,
                IsPlural                    INTEGER NULL,
                SingleVariant               VARCHAR(255) NULL,
                PluralVariant               VARCHAR(255) NULL,
                IsVerbPast                  INTEGER NULL,
                IsVerbPresent               INTEGER NULL,
                IsVerbFutur                 INTEGER NULL,
                VerbTense                   VARCHAR(255) NULL,
                Translation_EN              TEXT NULL,
                Translation_FR              TEXT NULL,
                Translation_DE              TEXT NULL,
                Translation_IT              TEXT NULL,
                Translation_ES              TEXT NULL,
                Translation_RU              TEXT NULL,
                Translation_PT              TEXT NULL,
                Ext_Wikipedia_URL           TEXT NULL,
                CountTotalOfWikipediaUrl    INTEGER NULL,
                ExplainationExamplesTxt     TEXT NULL,
                PopularityOfWord            INTEGER NULL,
        
                Instance_of                 TEXT NULL,              
                Subclass_of                 TEXT NULL,
                Part_of                     TEXT NULL,
                WikipediaLinkCountTotal     TEXT NULL,
                ExplainationTxt             TEXT NULL,

                Operation_Merging           INTEGER NULL,
                Operation_Wikipedia         INTEGER NULL,
                Operation_Vectorizer        INTEGER NULL,
                Operation_PropertiesInv     INTEGER NULL,
                Operation_VectSentences     INTEGER NULL,
                Operation_Pref              INTEGER NULL,
                LabelNamePreference         INTEGER NULL,
        
                FromWP                      TEXT NULL,
                FromWT                      TEXT NULL,
                FromWD                      TEXT NULL,
                FromCJ                      TEXT NULL, 
                MergedWith                  TEXT NULL, 

                Description_Vect            TEXT NULL,
                ExplainationTxt_Vect        TEXT NULL,
                AlsoKnownAs_Vect            TEXT NULL,
                Instance_of_Vect            TEXT NULL,
                Subclass_of_Vect            TEXT NULL,
                Part_of_Vect                TEXT NULL,
                AlternativeFormsOther_Vect  TEXT NULL,
                Synonymy_Vect               TEXT NULL,
                Antonymy_Vect               TEXT NULL,
                Hypernymy_Vect              TEXT NULL,
                Hyponymy_Vect               TEXT NULL,
                Meronymy_Vect               TEXT NULL,
                RelatedTerms_Vect           TEXT NULL,
                CoordinateTerms_Vect        TEXT NULL,
                Otherwise_Vect              TEXT NULL
            )
        """

    def __init__( self, parent=None ):
        self.PK                          = ""
        self.LabelName                   = ""
        self.LabelType                   = ""
        self.LanguageCode                = ""
        self.Type                        = ""
        self.IndexInPageWiktionary       = 0
        self.Description                 = ""
        self.DescriptionWikipediaLinks   = []
        self.DescriptionWiktionaryLinks  = []
        self.SelfUrlWikidata             = ""
        self.SelfUrlWiktionary           = ""
        self.SelfUrlWikipedia            = ""
        self.Synonymy                    = []
        self.Antonymy                    = []
        self.Hypernymy                   = []
        self.Hyponymy                    = []
        self.Holonymy                    = []
        self.Troponymy                   = []
        self.Meronymy                    = []
        self.SeeAlso                     = []
        self.SeeAlsoWikipediaLinks       = []
        self.RelatedTerms                = []
        self.AlsoKnownAs                 = []
        self.IsMale                      = None
        self.IsNeutre                    = None
        self.IsFeminine                  = None
        self.MaleVariant                 = ""
        self.FemaleVariant               = ""
        self.IsSingle                    = None
        self.IsPlural                    = None
        self.SingleVariant               = ""
        self.PluralVariant               = ""
        self.IsVerbPast                  = None
        self.IsVerbPresent               = None
        self.IsVerbFutur                 = None
        self.VerbTense                   = ""
        self.Translation_EN              = []
        self.Translation_FR              = []
        self.Translation_DE              = []
        self.Translation_IT              = []
        self.Translation_ES              = []
        self.Translation_RU              = []
        self.Translation_PT              = []
        self.Ext_Wikipedia_URL           = ""
        self.CountTotalOfWikipediaUrl    = 0
        self.ExplainationExamplesTxt     = []
        self.PopularityOfWord            = 0

        self.Instance_of                 = []
        self.Subclass_of                 = []
        self.Part_of                     = []
        self.WikipediaLinkCountTotal     = 0
        self.ExplainationTxt             = ""

        self.Operation_Merging           = 0
        self.Operation_Wikipedia         = 0
        self.Operation_Vectorizer        = 0
        self.Operation_PropertiesInv     = 0
        self.Operation_VectSentences     = 0
        self.Operation_Pref              = 0
        self.LabelNamePreference         = 0

        self.FromWP                      = [] # PK from Wikipedia
        self.FromWT                      = [] # PK from Wiktionary
        self.FromWD                      = [] # PK from Wikidict
        self.FromCJ                      = [] # PK from Conjugator
        self.MergedWith                  = []

        self.AlsoKnownAs_Vect            = []
        self.Instance_of_Vect            = []
        self.Subclass_of_Vect            = []
        self.Part_of_Vect                = []
        self.ExplainationTxt_Vect        = []
        self.AlternativeFormsOther_Vect  = []
        self.Synonymy_Vect               = []
        self.Antonymy_Vect               = []
        self.Hypernymy_Vect              = []
        self.Hyponymy_Vect               = []
        self.Meronymy_Vect               = []
        self.RelatedTerms_Vect           = []
        self.CoordinateTerms_Vect        = []
        self.Otherwise_Vect              = []

    def __repr__( self ):
        return f"Word({self.LabelName}: {self.PK})"
