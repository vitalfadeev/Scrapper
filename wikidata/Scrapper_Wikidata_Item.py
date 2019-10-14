#!/usr/bin/python3
# -*- coding: utf-8 -*-

class WikidataItem:
    class Meta:
        DB_TABLE_NAME = "wikidata"
        DB_INIT = """
            CREATE TABLE IF NOT EXISTS wikidata (
                PrimaryKey                 VARCHAR(255) NOT NULL PRIMARY KEY,
                SelfUrl                    VARCHAR(255),
                LabelName                  VARCHAR(255),
                LanguageCode               CHAR(2),
                CodeInWiki                 VARCHAR(255),
                Description                TEXT NULL,
                AlsoKnownAs                TEXT
                WikipediaENURL             VARCHAR(255),
                EncyclopediaBritannicaEN   VARCHAR(255),
                EncyclopediaUniversalisFR  VARCHAR(255),
                DescriptionUrl             VARCHAR(255),
                Instance_of                TEXT NULL,
                Subclass_of                TEXT NULL,
                Part_of                    TEXT NULL,
                Translation_EN             TEXT NULL,
                Translation_FR             TEXT NULL,
                Translation_DE             TEXT NULL,
                Translation_IT             TEXT NULL,
                Translation_ES             TEXT NULL,
                Translation_RU             TEXT NULL,
                Translation_PT             TEXT NULL,
                WikipediaLinkCountTotal    INTEGER,
                EncyclopediaGreatRussianRU VARCHAR(255)
            );
            
            CREATE INDEX IF NOT EXISTS  LanguageCode ON wiktidata (LanguageCode);
        """

    def __init__( self ):
        self.PrimaryKey = ""
        self.SelfUrl = ""
        self.LabelName = ""
        self.LanguageCode = ""
        self.CodeInWiki = ""
        self.Description = ""
        self.AlsoKnownAs = [ ]
        self.SelfUrl = ""
        self.WikipediaENURL = ""
        self.EncyclopediaBritannicaEN = ""
        self.EncyclopediaUniversalisFR = ""
        self.DescriptionUrl = ""
        self.Instance_of = [ ]
        self.Subclass_of = [ ]
        self.Part_of = [ ]
        self.Translation_EN = [ ]
        self.Translation_FR = [ ]
        self.Translation_DE = [ ]
        self.Translation_IT = [ ]
        self.Translation_ES = [ ]
        self.Translation_RU = [ ]
        self.Translation_PT = [ ]
        self.WikipediaLinkCountTotal = 0
        self.EncyclopediaGreatRussianRU = ""

    def __repr__( self ):
        return "WikidataItem(" + self.LabelName + ")"
