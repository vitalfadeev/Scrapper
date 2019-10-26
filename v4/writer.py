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


def Write( url, writers=None, encoding='UTF-8', streamed=False, *args ):
    return Writer()

