#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from collections.abc import Iterable
from Scrapper_Helpers import remove_comments, extract_from_link, filterWodsProblems

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class WikipediaItem:
    class Meta:
        DB_TABLE_NAME = "wiktionary"
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
                    SelfUrlWikipedia		    VARCHAR(255),
                    SeeAlso						TEXT,
                    SeeAlsoWikipediaLinks		TEXT,
                    ExplainationExamplesRaw		TEXT,
                    ExplainationExamplesTxt		TEXT
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
        self.SelfUrlWikipedia			 = ""
        self.SeeAlso			         = []
        self.SeeAlsoWikipediaLinks		 = []
        self.ExplainationExamplesRaw	 = []
        self.ExplainationExamplesTxt	 = []
            
    def __repr__(self):
        return "WikictionaryItem(" + self.LabelName + ': ' + self.PrimaryKey + ")"


