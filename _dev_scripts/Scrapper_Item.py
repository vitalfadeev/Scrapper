import math
import re


class Str( str ):
    def len( self ):
        return len( self )

    def get_words( self ) -> "List":
        words = re.split( "\W+", self )
        return List( words )

    def InitalUpperCase( self ):
        return self[0].upper() + self[1:].lower()


class Int( int ):
    def sqrt( self ):
        return math.sqrt( self )


class List( list ):
    def count( self ):
        return Int( len( self ) )

    def filter( self, fn ) -> "Iter":
        return Iter( filter( fn, self ) )

    def map( self, fn ) -> "Iter":
        return Iter( map( fn, self ) )

    def each( self, fn ) -> "Iter":
        return Iter( map( fn, self ) )

    def join( self, s ) -> Str:
        return s.join( self )


#from collections.abc import Iterable
class Iter:
    def __init__(self, obj):
        self._obj = obj

    def count( self ):
        return Int( len( self ) )

    def filter( self, fn ) -> "Iter":
        return Iter( filter( fn, self ) )

    def __iter__(self):
        return self

    def __next__(self):
        return next( self._obj )


class ItemProxy:
    def __init__( self, o ):
        self.__dict__[ '_o' ] = o

    def __getattr__( self, name ):
        if hasattr( self.__dict__[ '_o' ], name ):
            a = getattr( self.__dict__[ '_o' ], name )

            if isinstance( a, str ):
                return Str( a )
            elif isinstance( a, list ):
                return List( a )
            elif isinstance( a, int ):
                return Int( a )
            else:
                return a

    def __setattr__( self, name, value ):
        setattr( self.__dict__[ '_o' ], name, value )

