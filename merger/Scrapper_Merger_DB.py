import sqlite3

from Scrapper_DB import DBExecuteScript
from merger.Scrapper_Merger_Item import WordItem

DBWord = sqlite3.connect( "word.db", timeout=5.0 )
DBExecuteScript( DBWord, WordItem.Meta.DB_INIT )
