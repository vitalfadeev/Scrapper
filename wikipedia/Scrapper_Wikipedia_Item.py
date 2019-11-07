#!/usr/bin/python3
# -*- coding: utf-8 -*-

class WikipediaItem:
    class Meta:
        DB_TABLE_NAME = "wikipedia"
        DB_INIT = """
            CREATE TABLE IF NOT EXISTS wikipedia (
                    PK		                    VARCHAR(255) NOT NULL PRIMARY KEY,
                    LabelName                   VARCHAR(255),
                    LabelTypeWP                 VARCHAR(255),
                    LanguageCode                CHAR(2),
                    ExplainationWPTxt           TEXT,
                    ExplainationWPRaw           TEXT,
                    DescriptionWikipediaLinks   TEXT,
                    DescriptionWiktionaryLinks  TEXT,
                    DescriptionWikidataLinks    TEXT,
                    SelfUrlWikipedia		    VARCHAR(255),
                    SeeAlso						TEXT,
                    SeeAlsoWikipediaLinks		TEXT,
                    SeeAlsoWiktionaryLinks		TEXT,
                    ExplainationExamplesRaw		TEXT,
                    ExplainationExamplesTxt		TEXT,
                    LabelNamePreference    		INTEGER, 
                    Operation_Merging    		INTEGER, 
                    Operation_Pref       		INTEGER,
                    Operation_Vectorizer   		INTEGER 
            );
            
            -- CREATE INDEX IF NOT EXISTS  LanguageCode ON wikipedia (LanguageCode);
        """

    def __init__(self):
        self.PK			                 = ""
        self.LabelName			         = ""
        self.LabelTypeWP			     = ""
        self.LanguageCode			     = ""
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

        self.LabelNamePreference         = 0
        self.Operation_Merging           = 0
        self.Operation_Pref              = 0
        self.Operation_Vectorizer        = 0

    def __repr__(self):
        return f"WikipediaItem({self.LabelName}: {self.PK})"



