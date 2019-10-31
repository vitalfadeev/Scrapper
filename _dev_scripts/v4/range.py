import functools
import itertools
import re
import sqlite3

from . import writer


class Range:
    def __init__( self, iterable ):
        self.iterable = iterable  # iterable like list, str, file object, ioStream

    def __next__(self):
        return next( self.iterable )


    def __iter__(self):
        return self


    def by_element( self, name ):
        return Range( self.iterable )


    def by_line( self, eol='\n' ):
        return Range( itertools.takewhile( lambda c: c != eol, self.iterable ) )


    def all( self ):
        return Range( self.iterable )


    def head( self, n ):
        return Range( itertools.islice( self, 0, n ) )


    def convert( self, converter, workers=1 ):
        assert callable( converter )

        for row in self.iterable:
            return Range( converter( row ) )


    def filter( self, fn ):
        assert callable( fn )
        return Range( filter( fn, self.iterable ) )


    def write( self, url, *args, **kwargs ):
        from . import writer
        writer_instance = writer.get_writer( url, *args, **kwargs )
        writer_instance.write( self, *args, **kwargs )


    def map( self, fn ):
        assert callable( fn )
        return Range( map( fn, self.iterable ) )


    def generate( self, fn ):
        assert callable( fn )
        generated = ( fn( x ) for x in self.iterable )
        return Range( generated )


    def get_words( self ):
        words = re.split( "\W+", self.iterable )
        return Range( words )


    def join( self, s:str ) -> str:
        return s.join( self.iterable )


    def from_table( self, table, *args, **kwargs ):
        assert isinstance( sqlite3.Connection, self.iterable )
        sql = """
            SELECT * 
              FROM {table}
        """.format(
            table=table
        )

        where = kwargs.get( "where", None )

        #
        if where is not None:
            sql = sql + " WHERE " + where

        connection = self.iterable
        cursor = connection.cursor()
        query_result = cursor.execute( sql, args )

        return R( query_result )


    def from_sql( self, sql, *params, **kwargs ):
        assert isinstance( self.iterable, sqlite3.Connection ), "expect sqlite3.Connection"

        connection = self.iterable
        cursor = connection.cursor()
        query_result = cursor.execute( sql, params )

        # convert result to object | list | dict | ...
        cls = kwargs.get( "cls", None )

        if cls is tuple:
            result = query_result

        elif cls is list:
            result = query_result

        elif cls is dict:
            def convert_to_dict( row ):
                return dict.fromkeys( query_result.description, query_result )

            fn = functools.partial( convert_to_dict, query_result.description )

            result = map( fn, query_result )

        else:
            def convert_to_cls( cls, row ):
                o = cls()
                o.__dict__.update( dict.fromkeys( query_result.description, row ) )
                return o

            fn = functools.partial( convert_to_cls, cls )

            result = map( fn, query_result )

        return R( result )


    def to_object( self, cls ):
        o = cls()
        o.__dict__.update( self.iterable )
        return o


    def first( self ):
        return next( itertools.islice( self.iterable, 0, 1) )


    def as_list( self ):
        return list( self.iterable )


    def __getitem__( self, v ):
        if isinstance( v, slice ):
            return Range( itertools.islice( self, v.start, v.stop ) )

        elif isinstance( v, int ):
            return Range( itertools.islice( self, v, v+1 ) )

R = Range
