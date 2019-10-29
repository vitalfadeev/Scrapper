class WordItem:
    class Meta:
        DB_TABLE_NAME = "words"
        DB_INIT = """
            CREATE TABLE IF NOT EXISTS words (
                PrimaryKey                 VARCHAR(255) NOT   NULL  PRIMARY KEY,
                LabelName                  VARCHAR(255) NULL,
                LabelTypeWD                VARCHAR(255) NULL,
                LanguageCode               CHAR(2),
                Description                TEXT         NULL,
                AlsoKnownAs                TEXT         NULL,
                SelfUrlWikidata            VARCHAR(255) NULL,
                Instance_of                TEXT         NULL,
                Subclass_of                TEXT         NULL,
                Part_of                    TEXT         NULL,
                Translation_EN             TEXT         NULL,
                Translation_FR             TEXT         NULL,
                Translation_DE             TEXT         NULL,
                Translation_IT             TEXT         NULL,
                Translation_ES             TEXT         NULL,
                Translation_RU             TEXT         NULL,
                Translation_PT             TEXT         NULL,
                Ext_Wikipedia_URL          TEXT         NULL,
                CountTotalOfWikipediaUrl   INTEGER      NULL,
                Operation_Merging          INTEGER      NULL,
                Operation_Wikipedia        INTEGER      NULL,
                Operation_Vectorizer       INTEGER      NULL,
                Operation_PropertiesInv    INTEGER      NULL,
                Operation_VectSentences    INTEGER      NULL,
                Operation_Pref             INTEGER      NULL,
                Type                       VARCHAR(255) NULL,
                IndexInPageWiktionary      INTEGER      NULL,
                ExplainationTxt            VARCHAR(255) NULL,
                ExplainationRaw            VARCHAR(255) NULL,
                DescriptionWikipediaLinks  TEXT         NULL,
                DescriptionWiktionaryLinks TEXT         NULL,
                AlternativeFormsOther      TEXT         NULL,
                SelfUrlWiktionary          VARCHAR(255) NULL,
                Synonymy                   TEXT         NULL,
                Antonymy                   TEXT         NULL,
                Hypernymy                  TEXT         NULL,
                Hyponymy                   TEXT         NULL,
                Meronymy                   TEXT         NULL,
                RelatedTerms               TEXT         NULL,
                CoordinateTerms            TEXT         NULL,
                Otherwise                  TEXT         NULL,
                ExplainationExamplesRaw    TEXT         NULL,
                ExplainationExamplesTxt    TEXT         NULL,
                IsMale                     INTEGER      NULL,
                IsFeminine                 INTEGER      NULL, 
                IsNeutre                   INTEGER      NULL,
                IsSingle                   INTEGER      NULL,
                IsPlural                   INTEGER      NULL,
                SingleVariant              VARCHAR(255) NULL,
                PluralVariant              VARCHAR(255) NULL,
                MaleVariant                VARCHAR(255) NULL,
                FemaleVariant              VARCHAR(255) NULL,
                IsVerbPast                 INTEGER      NULL,
                IsVerbPresent              INTEGER      NULL,
                IsVerbFutur                INTEGER      NULL,
                VerbInfinitive             VARCHAR(255) NULL,
                VerbTense                  VARCHAR(255) NULL,
                LabelTypeWP                VARCHAR(255) NULL,
                ExplainationWPTxt          VARCHAR(255) NULL,
                ExplainationWPRaw          VARCHAR(255) NULL,
                DescriptionWikidataLinks   TEXT         NULL,
                SelfUrlWikipedia           VARCHAR(255) NULL,
                SeeAlso                    TEXT         NULL,
                SeeAlsoWikipediaLinks      TEXT         NULL,
                SeeAlsoWiktionaryLinks     TEXT         NULL
            )
        """

    def __init__( self, parent=None ):
        # Wikidata
        self.PK                        = ""
        self.LabelName                 = ""
        self.LabelTypeWD               = ""
        self.LanguageCode              = ""
        self.Description               = ""
        self.AlsoKnownAs               = ""
        self.SelfUrlWikidata           = ""
        self.Instance_of               = [ ]
        self.Subclass_of               = [ ]
        self.Part_of                   = [ ]
        self.Translation_EN            = [ ]
        self.Translation_FR            = [ ]
        self.Translation_DE            = [ ]
        self.Translation_IT            = [ ]
        self.Translation_ES            = [ ]
        self.Translation_RU            = [ ]
        self.Translation_PT            = [ ]
        #
        self.Ext_Wikipedia_URL         = ""
        self.CountTotalOfWikipediaUrl  = 0
        #
        self.Operation_Merging         = 0
        self.Operation_Wikipedia       = 0
        self.Operation_Vectorizer      = 0
        self.Operation_PropertiesInv   = 0
        self.Operation_VectSentences   = 0
        self.Operation_Pref            = 0

        # Wiktionary
        self.LabelType                   = ""  #
        self.Type                        = ""  #                        = noun,verb… see = WORD_TYPES
        self.IndexInPageWiktionary       = 0
        self.ExplainationTxt             = ""  #
        self.ExplainationRaw             = ""  #
        self.DescriptionWikipediaLinks   = []
        self.DescriptionWiktionaryLinks  = []
        self.AlternativeFormsOther       = []
        self.SelfUrlWiktionary           = ""
        self.Synonymy                    = []
        self.Antonymy                    = []
        self.Hypernymy                   = []
        self.Hyponymy                    = []
        self.Meronymy                    = []
        self.RelatedTerms                = []
        self.CoordinateTerms             = []
        self.Otherwise                   = []
        self.ExplainationExamplesRaw     = []
        self.ExplainationExamplesTxt     = []
        self.IsMale                      = bool
        self.IsFeminine                  = bool  # ""
        self.IsNeutre                    = bool  # ""
        self.IsSingle                    = bool
        self.IsPlural                    = bool
        self.SingleVariant               = ""  # ""
        self.PluralVariant               = ""  # ""
        self.MaleVariant                 = ""  # ""
        self.FemaleVariant               = ""  # ""
        self.IsVerbPast                  = bool
        self.IsVerbPresent               = bool
        self.IsVerbFutur                 = bool
        #
        self.VerbInfinitive              = ""
        self.VerbTense                   = ""

        # Wikipedia
        self.LabelTypeWP			     = ""
        self.ExplainationWPTxt			 = ""
        self.ExplainationWPRaw			 = ""
        self.DescriptionWikipediaLinks   = []
        self.DescriptionWiktionaryLinks  = []
        self.DescriptionWikidataLinks    = []
        self.SelfUrlWikipedia			 = ""
        self.SeeAlso			         = []
        self.SeeAlsoWikipediaLinks		 = []
        self.SeeAlsoWiktionaryLinks 	 = []
        self.ExplainationExamplesRaw	 = []
        self.ExplainationExamplesTxt	 = []

        # Conjugations
        # ...


    def __repr__( self ):
        return "Word(" + self.LabelName + ")"
