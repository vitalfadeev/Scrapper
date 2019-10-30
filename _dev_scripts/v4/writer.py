import sqlite3


class Writer:
    def element( self ):
        ...

    def line( self ):
        ...

    def all( self ):
        ...

    def write( self ):
        ...

    def item( self ):
        ...

    def __call__(self, *args, **kwargs):
        ...


def get_writer( url, *args, **kwargs ):
    # writer factory
    if isinstance( url, str ):
        ...

    elif isinstance( url, sqlite3.Connection ):
        from .writers.sqlite3 import Writer
        return Writer( url )

    else:
        assert 0, "unsupported"


def Write( url, writers=None, encoding='UTF-8', streaming=False, *args ):
    return Writer()


def write( url, writers=None, encoding='UTF-8', streaming=False, *args ):
    return Writer()

