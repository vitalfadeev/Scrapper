import io
import bz2
from . import file_binary


def Reader( f ):
    if isinstance( f, str ):
        # open file
        url = f
        #
        with Reader( url ) as reader:
            # open bz2
            with bz2.open( reader ) as stream:
                return stream

    elif isinstance( f, io.IOBase ):
        # use bz2 file object
        file_object = f
        # open bz2
        with bz2.open( file_object ) as stream:
            return stream
