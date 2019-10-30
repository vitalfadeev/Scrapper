import functools
import io
import os
import importlib
import sqlite3
from contextlib import contextmanager
from urllib.parse import urlparse
from .range import Range, R


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

def read_sqlite( db, table=None, sql=None, cls=None, *args, **kwargs ):
    assert isinstance( db, sqlite3.Connection ), "expect sqlite3.Connection"

    connection = db

    if sql is None:
        sql = """
        SELECT *
          FROM {table}
        """.format(
            table=table,
        )

    cursor = connection.cursor()
    query_result = cursor.execute( sql, args )

    # convert result to object | list | dict | ...
    if cls is tuple:
        result = query_result

    elif cls is list:
        result = query_result

    elif cls is dict:
        def convert_to_dict( fields, row ):
            return dict( zip( fields, row ) )

        fields = [ x[0] for x in query_result.description ]
        fn = functools.partial( convert_to_dict, fields )

        result = map( fn, query_result )

    else:
        def convert_to_cls( cls, fields, row ):
            o = cls()
            o.__dict__.update( dict( zip( fields, row ) ) )
            return o

        fields = [ x[0] for x in query_result.description ]
        fn = functools.partial( convert_to_cls, cls, fields )

        result = map( fn, query_result )

    return R( result )


def read( src, *args, **kwargs ):
    if isinstance( src, sqlite3.Connection ):
        return read_sqlite( src, *args, **kwargs )



# pass to last reader 'dump.xml.bz2'
# pass to reader opened stream
def Read( url, readers=None, encoding='UTF-8', streaming=False, caching=False ):
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
