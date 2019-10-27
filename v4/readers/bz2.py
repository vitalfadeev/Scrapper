import io
import bz2
from . import file_binary


def Reader( f: io.FileIO, url ):
    # use bz2 file object
    file_object = f
    # open bz2
    return bz2.open( file_object )
