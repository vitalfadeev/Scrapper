import functools
import io
import json
import os
import importlib
import sqlite3
from urllib.parse import urlparse
from .range import Range


# Example: 'dump.xml.bz2'
# 1. get extension: 'bz2'
# 2. find reader module: reader/bz2.py
# 3. get rest extension: 'xml'
# 4. find reader module: reader/xml.py
# 5. get rest extension: ''
# 6. if ''
#    pass to xml.reader( 'dump.xml.bz2' )
#
# def read( *args, **kvargs ):
#     return Read( *args, **kvargs )

def read_sqlite( db, table=None, sql=None, cls=None, params=None, *args, **kwargs ):
    assert isinstance( db, sqlite3.Connection ), "expect sqlite3.Connection"

    connection = db

    #
    if sql is None:
        sql = f""" SELECT * FROM {table} """

    #
    if params is None:
        params = args

    # execute
    cursor = connection.cursor()
    query_result = cursor.execute( sql, params )

    # convert result to object | list | dict | ...
    if cls is None:
        result = query_result

    elif cls is tuple:
        result = query_result

    elif cls is list:
        result = query_result

    elif cls is dict:
        def convert_to_dict( fields, row ):
            return dict( zip( fields, row ) )

        fields = [ x[0] for x in query_result.description ]
        fn = functools.partial( convert_to_dict, fields )

        result = map( fn, query_result )

    else: # cls is class
        def convert_to_cls( cls, fields, row ):
            # str -> str
            #     -> []
            #     -> {}
            # int -> int
            # nul -> str
            #     -> []
            #     -> {}
            #     -> int
            # depends of cls.attr type

            o = cls()

            for field, value in dict( zip( fields, row ) ):
                a = getattr( o, field )

                if value is None:
                    pass
                else:
                    if isinstance( a, list ):
                        setattr( o, field, json.loads( value ) )

                    elif isinstance( a, dict ):
                        setattr( o, field, json.loads( value ) )

                    else:
                        setattr( o, field, value )

            return o

        fields = [ x[0] for x in query_result.description ]
        fn = functools.partial( convert_to_cls, cls, fields )

        result = map( fn, query_result )

    return Range( result )


def read( src, *args, **kwargs ):
    if isinstance( src, sqlite3.Connection ):
        return read_sqlite( src, *args, **kwargs )



# pass to last reader 'dump.xml.bz2'
# pass to reader opened stream
def Read( url, readers=None, encoding='UTF-8', streaming=False, caching=False, *args, **kwargs ) -> Range:
    """
    Read data source. See examples below.

    Args:
        url:
        readers:
        encoding:
        streaming:
        caching:

    Returns:
        Range

    ::

        from read import Read

        # 1
        Read( 'dump.xml.bz2' )

        # 2
        Read( 'dump.xml' )

        # 3
        Read( 'dump.txt' )

        # 4
        Read( 'dump.ini' )

        # 5
        Read( 'dump.json' )

        # 6
        Read( 'dump.json.bz2' )

        # 7
        Read( 'http://api.ixioo.com/PKS_Match' )

        # 8
        Read( 'words.db' )

        # 9
        Read( 'words.sqlite' )

        # 10
        Read( 'words.db', table="words" )

        # 11
        Read( 'words.db', table="words", where="LabelName = ? ", "Cat" )

        # 12
        Read( 'words.db', sql="SELECT * FROM words WHERE LabelName = ? ", "Cat" )
        Read( 'words.db', sql="SELECT * FROM words WHERE LabelName = ? ", params=["Cat"] )

        # 13
        Read( 'words.db', table="words", cls=WordItem )

        # 14
        class WordItem:
            _database = 'words.db'
            _table = 'words'

            def __init( self ):
                self.PK = ""
                self.LabelName = ""

        Read( WordItem )

        # 15
        Read( WordItem, sql="SELECT * FROM words WHERE LabelName = ? ", "Cat" )

        # 16
        DBWORDS = 'words.db'
        Read( DBWORDS, "SELECT * FROM words WHERE LabelName = ? ", "Cat" )

        # 17
        for w in Read( DBWORDS ):
            print( w )

        # 18
        Read( DBWORDS ).map( ... ).write( DBWORDS )

        # 19
        Read( "SELECT * FROM words WHERE LabelName = ? ", "Cat" ).as_object( WordItem )
        Read( "SELECT * FROM words WHERE LabelName = ? ", "Cat" ).as_dict()
        Read( "SELECT * FROM words WHERE LabelName = ? ", "Cat" ).as_list()
        Read( "SELECT * FROM words WHERE LabelName = ? ", "Cat" ).as_tuple()

    """
    if isinstance( url, str ):
        return read_str( url, *args, **kwargs )

    elif isinstance( url, object ):
        cls = url
        return read_class( cls, *args, **kwargs )


def read_str( url, *args, **kwargs ):
    url_upper = url.upper()

    if url_upper.startswith( "SELECT "):
        return read_sql( url, *args, **kwargs )

    elif url_upper.startswith( "HTTP://" ):
        return read_http( url, *args, **kwargs )

    elif url_upper.startswith( "HTTPS://" ):
        return read_http( url, *args, **kwargs )

    else:
        return read_str_other( url, *args, **kwargs )


def read_str_other( url, readers=None, encoding='UTF-8', streaming=False, caching=False, *args, **kwargs ):
    parsed = urlparse( url )
    scheme = parsed.scheme
    path = parsed.path

    # '' -> file
    if scheme == '':
        scheme = 'file'

    # package = '.readers.scheme'
    # scheme_module = importlib.import_module( scheme, package )
    #
    # with scheme_module.Reader() as scheme_reader:
    #     return scheme_reader

    classes = get_reader_class( url )

    f = io.FileIO( path )

    wf = wrap( f, url, classes )

    return Range( wf )


def read_class( cls, readers=None, encoding='UTF-8', streaming=False, caching=False, *args, **kwargs ):
    return Range( [] )


def read_sql( sql, readers=None, encoding='UTF-8', streaming=False, caching=False, *args, **kwargs ):
    return Range( [] )


def read_http( url, readers=None, encoding='UTF-8', streaming=False, caching=False, *args, **kwargs ):
    return Range( [] )



def wrap( f, url, classes ):
    if classes:
        cls = classes[0]

        wf = cls( f, url )

        return wrap( wf, url, classes[1:] )

    else:
        return f


def get_reader_class( url ):
    classes = []

    # next
    filename, file_extension = os.path.splitext( url )

    if file_extension:
        # find reader
        package = 'v4.readers'
        reader_module_name = file_extension[1:] # remove dot. '.xml' -> 'xml'
        module = importlib.import_module( package + '.' + reader_module_name )

        print(module)

        cls = module.Reader
        classes.append( cls )

        # recursive
        if filename:
            classes.extend( get_reader_class( filename ) )

    return classes
