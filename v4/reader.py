import os
import importlib
from urllib.parse import urlparse


# Example: 'dump.xml.bz2'
# 1. get extension: 'bz2'
# 2. find reader module: reader/bz2.py
# 3. get rest extension: 'xml'
# 4. find reader module: reader/xml.py
# 5. get rest extension: ''
# 6. if ''
#    pass to xml.reader( 'dump.xml.bz2' )
#

# pass to last reader 'dump.xml.bz2'
# pass to reader opened stream

def Reader( url ):
    parsed = urlparse( url )
    scheme = parsed.scheme
    path = parsed.path

    # '' -> file
    if scheme == '':
        scheme = 'file'

    package = '.readers.scheme'
    scheme_module = importlib.import_module( scheme, package )

    with scheme_module.Reader() as scheme_reader:
        return scheme_reader


    # next
    filename, file_extension = os.path.splitext( url )

    if file_extension:
        # find reader
        package = '.readers'
        reader_module_name = file_extension[1:] # remove dot. '.xml' -> 'xml'
        module = importlib.import_module( reader_module_name, package )

        with module.Reader( scheme_reader ) as stream:
            return stream

