#!/usr/bin/python3
# -*- coding: utf-8 -*-

class ConjugationsItem:
    class Meta:
        DB_TABLE_NAME = "conjugations"
        DB_INIT = """
            CREATE TABLE IF NOT EXISTS conjugations (
                    PK		                    VARCHAR(255) NOT NULL PRIMARY KEY,
                    LabelName                   VARCHAR(255),
                    LabelType                   VARCHAR(255),
                    LanguageCode                CHAR(2),
                    Type                        VARCHAR(255),
                    ExplainationTxt		        TEXT NULL,
                    AlternativeFormsOther       TEXT NULL,
                    OtherwiseRelated            TEXT NULL,
                    IsMale                      INTEGER NULL,
                    IsFeminine                  INTEGER NULL,
                    IsSingle                    INTEGER NULL,
                    IsPlural                    INTEGER NULL,
                    SingleVariant               VARCHAR(255),
                    PluralVariant               VARCHAR(255),
                    IsVerbPast                  INTEGER NULL,
                    IsVerbPresent               INTEGER NULL,
                    IsVerbFutur                 INTEGER NULL,
                    Operation_Merging    		INTEGER, 
                    Operation_Pref       		INTEGER 
            );
            
            -- CREATE INDEX IF NOT EXISTS  LanguageCode ON conjugations (LanguageCode);
        """

    def __init__(self):
        self.PK			                 = ""
        self.LabelName			         = ""
        self.LabelType   			     = ""
        self.LanguageCode			     = ""
        self.Type       			     = ""
        self.ExplainationTxt		     = ""
        self.AlternativeFormsOther       = []
        self.OtherwiseRelated            = []
        self.IsMale                      = bool
        self.IsFeminine                  = bool
        self.IsSingle                    = bool
        self.IsPlural                    = bool
        self.SingleVariant               = ""
        self.PluralVariant               = ""
        self.IsVerbPast                  = bool
        self.IsVerbPresent               = bool
        self.IsVerbFutur                 = bool
        self.LabelNamePreference         = 0
        self.Operation_Merging           = 0
        self.Operation_Pref              = 0

    def __repr__(self):
        return "ConjugationsItem(" + self.LabelName + ': ' + self.PK + ")"



