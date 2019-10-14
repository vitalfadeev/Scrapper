class WordItem:
    class Meta:
        DB_TABLE_NAME = "words"
        DB_INIT = """
            CREATE TABLE IF NOT EXISTS words (
                PrimaryKey                VARCHAR(255) NOT NULL PRIMARY KEY,
                LabelName                 VARCHAR(255),
                CodeInWiki                VARCHAR(255),
                LanguageCode              VARCHAR(255),
                Description               TEXT NULL,
                AlsoKnownAs               TEXT NULL,
                SelfUrl                   VARCHAR(255),
                WikipediaENURL            VARCHAR(255),
                EncyclopediaBritannicaEN  VARCHAR(255),
                EncyclopediaUniversalisEN VARCHAR(255),
                Instance_of               TEXT NULL,
                Subclass_of               TEXT NULL,
                Part_of                   TEXT NULL,
                Translation_EN            TEXT NULL,
                Translation_FR            TEXT NULL,
                Translation_DE            TEXT NULL,
                Translation_IT            TEXT NULL,
                Translation_ES            TEXT NULL,
                Translation_RU            TEXT NULL,
                Translation_PT            TEXT NULL,
                #
                LabelType                 VARCHAR(255),
                Type                      VARCHAR(255),
                Explaination              VARCHAR(255),
                ExplainationExamples      TEXT NULL,
                IsMale                    VARCHAR(255),
                IsFeminine                VARCHAR(255),
                IsSingle                  VARCHAR(255),
                IsPlural                  VARCHAR(255),
                SingleVariant             VARCHAR(255),
                PluralVariant             VARCHAR(255),
                IsVerbPast                VARCHAR(255),
                IsVerbPresent             VARCHAR(255),
                IsVerbFutur               VARCHAR(255),
                Conjugation               TEXT NULL,
                Synonymy                  TEXT NULL,
                Antonymy                  TEXT NULL,
                Hypernymy                 TEXT NULL,
                Hyponymy                  TEXT NULL,
                Meronymy                  TEXT NULL,
                Holonymy                  TEXT NULL,
                Troponymy                 TEXT NULL,
                Otherwise                 TEXT NULL,
                AlternativeFormsOther     TEXT NULL,
                RelatedTerms              TEXT NULL,
                Coordinate                TEXT NULL,
                #
                WikipediaENContent        VARCHAR(255),
                BritannicaENContent       VARCHAR(255),
                UniversalisENContent      VARCHAR(255)
            );

            CREATE INDEX IF NOT EXISTS  LanguageCode ON words (LanguageCode);
        """

    def __init__( self, parent=None ):
        self.PrimaryKey                = ""
        self.LabelName                 = ""
        self.CodeInWiki                = ""
        self.LanguageCode              = ""
        self.Description               = ""
        self.AlsoKnownAs               = ""
        self.SelfUrl                   = ""
        self.WikipediaENURL            = ""
        self.EncyclopediaBritannicaEN  = ""
        self.EncyclopediaUniversalisEN = ""
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
        self.LabelType                 = ""
        self.Type                      = ""
        self.Explaination              = ""
        self.ExplainationExamples      = [ ]
        self.IsMale                    = ""
        self.IsFeminine                = ""
        self.IsSingle                  = ""
        self.IsPlural                  = ""
        self.SingleVariant             = ""
        self.PluralVariant             = ""
        self.IsVerbPast                = ""
        self.IsVerbPresent             = ""
        self.IsVerbFutur               = ""
        self.Conjugation               = [ ]
        self.Synonymy                  = [ ]
        self.Antonymy                  = [ ]
        self.Hypernymy                 = [ ]
        self.Hyponymy                  = [ ]
        self.Meronymy                  = [ ]
        self.Holonymy                  = [ ]
        self.Troponymy                 = [ ]
        self.Otherwise                 = [ ]
        self.AlternativeFormsOther     = [ ]
        self.RelatedTerms              = [ ]
        self.Coordinate                = [ ]
        #
        self.WikipediaENContent        = ""
        self.BritannicaENContent       = ""
        self.UniversalisENContent      = ""

        # inherit from parent
        if parent:
            for f in vars(self):
                setattr( self, f, getattr( parent, f ) )

    def __repr__( self ):
        return "Word(" + self.LabelName + ")"
