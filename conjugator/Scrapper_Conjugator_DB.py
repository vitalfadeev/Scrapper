import sqlite3

from Scrapper_DB import DBExecuteScript
from conjugator.Scrapper_Conjugations_Item import ConjugationsItem

DB_NAME         = "conjugations.db"
DBConjugations  = sqlite3.connect( DB_NAME, timeout=5.0 )
# init DB
DBExecuteScript( DBConjugations, ConjugationsItem.Meta.DB_INIT )

