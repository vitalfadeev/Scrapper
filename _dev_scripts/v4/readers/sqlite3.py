import io
import sqlite3

def Reader( f, url, stream=False, tag=None ):
    db = sqlite3.connect( url )
    c = db.cursor()
    rows = c.execute("select * from wikipedia")
    return rows

