import sqlite3

from Scrapper_DB import DBExecuteScript
from wiktionary.Scrapper_Wiktionary_Item import WiktionaryItem

DB_NAME         = "wiktionary.db"
DBWiktionary  = sqlite3.connect( DB_NAME, timeout=5.0 )
# init DB
DBExecuteScript( DBWiktionary, WiktionaryItem.Meta.DB_INIT )

