import sqlite3

from Scrapper_DB import DBExecuteScript
from wikidata.Scrapper_Wikidata_Item import WikidataItem

DB_NAME      = "wikidata.db"
DBWikidata  = sqlite3.connect( DB_NAME, timeout=5.0 )
# init DB
DBExecuteScript( DBWikidata, WikidataItem.Meta.DB_INIT )

