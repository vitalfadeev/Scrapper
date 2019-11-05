import sqlite3

from Scrapper_DB import DBExecuteScript
from wikipedia.Scrapper_Wikipedia_Item import WikipediaItem

DB_NAME         = "wikipedia.db"
DBWikipedia     = sqlite3.connect( DB_NAME, timeout=5.0 )
# init DB
DBExecuteScript( DBWikipedia, WikipediaItem.Meta.DB_INIT )

