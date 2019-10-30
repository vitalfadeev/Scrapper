import sqlite3

from Scrapper_DB import DBWrite
from _dev_scripts.v4.range import Range
from merger.Scrapper_Merger_Item import WordItem


class Writer:
    def __init__(self, db: sqlite3.Connection ):
        assert isinstance( db, sqlite3.Connection )
        self.db = db

    def write( self, iterable: Range, table: str=None, pk: str="PrimaryKey", if_exists: str="fail", *args, **kwargs ):
        assert isinstance( iterable, Range )

        # #
        # if if_exists == "replace":
        #     mode = "OR REPLACE"
        #
        # elif if_exists == "fail":
        #     mode = "OR FAIL"
        #
        # elif if_exists == "ignore":
        #     mode = "OR IGNORE"
        #
        # else:
        #     mode = ""
        #
        # #
        # fields = [ ]
        # values = [ ]
        # placeholders = [ ]

        for item in iterable:
            if isinstance( item, WordItem ):
                DBWrite( self.db, item, table=table, if_exists=if_exists, *args, **kwargs )

            #     fields = [ f for f in vars( item ) if not callable( f ) and not f.startswith('_') and f[0].isupper() ]
            #     values = [ getattr( item, f ) for f in fields ]
            #     placeholders = "?" * len( fields )
            #
            #     fields_str = ",".join( fields )
            #     placeholders_str = ",".join( placeholders )
            #
            # sql = """
            # INSERT {mode} INTO {table} ({fields})
            #      VALUES ({placeholders})
            # """.format(
            #     mode=mode,
            #     table=table,
            #     fields=fields_str,
            #     placeholders=placeholders_str,
            # )
            #
            # print( item )
            # print( type(item) )
            # print( values[8] )
            #
            # self.db.execute( sql, values )
            # self.db.commit()
            #
