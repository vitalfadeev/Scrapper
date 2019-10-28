import itertools
from . import writer


class Range:
    def __init__( self, f ):
        self.f = f

    def __next__(self):
        return next( self.f )


    def __iter__(self):
        return self


    def by_element( self, name ):
        return Range( self.f )


    def by_line( self, eol='\n' ):
        return Range( itertools.takewhile( lambda c: c != eol, self.f ) )


    def all( self ):
        return Range( self.f )


    def head( self, n ):
        return Range( itertools.islice( self, 0, n ) )


    def convert( self, converter, workers=1 ):
        assert callable( converter )

        for row in self.f:
            return Range( converter( row ) )


    def filter( self ):
        return Range( self.f )


    def write( self, url ):
        for item in self.f:
            writer.write( url, item )


    def __getitem__( self, v ):
        if isinstance( v, slice ):
            return Range( itertools.islice( self, v.start, v.stop ) )

        elif isinstance( v, int ):
            return Range( itertools.islice( self, v, v+1 ) )
