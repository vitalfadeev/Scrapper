#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import io
import pickle
import json
import logging
import collections
import time
import functools
from typing import Iterator

log = logging.getLogger(__name__)


def create_storage(folder_name):
    """
    Create folders recusively.

    In:
      folder_name: Storage folder name

    """
    if (not os.path.exists(folder_name)):
        os.makedirs(folder_name, exist_ok=True)


def sanitize_filename(filename):
    """
    Remove from string 'filename' all nonascii chars and  punctuations.
    """
    filename = str(filename)
    filename = "".join(x if x.isalnum() else "_" for x in filename)

    # fixes
    if filename.lower() == "con":
        filename = "reserved_con"

    elif filename.lower() == "aux":
        filename = "reserved_aux"

    elif filename.lower() == "prn":
        filename = "reserved_prn"

    return filename


def unique( lst: Iterator ) -> list:
    """
    Unique list items.

    Source list keeps unchanged.

    Args:
        lst (list):  List with items

    Returns:
        (list)

    ::

        >>> import Scrapper_Helpers
        >>> Scrapper_Helpers.unique([1,1,1,2,3])
        [1, 2, 3]

    """
    qniqued = list ( collections.OrderedDict.fromkeys( lst ).keys() )
    return qniqued


def get_contents( filename: str ) -> str:
    """
    Read the file 'filename' and return content.

    ::

        >>> with open('checkpoint.txt' , 'w') as f:
        >>>    f.write( 'test data')

        >>> import Scrapper_Helpers
        >>> Scrapper_Helpers.get_contents( 'checkpoint.txt' )
        'test data'

    """
    with open(filename, 'rt', encoding="UTF-8") as f:
        return f.read()


def put_contents(filename, content):
    """
    Save 'content' to the file 'filename'. UTF-8.

    ::

        >>> import Scrapper_Helpers
        >>> Scrapper_Helpers.put_contents( 'checkpoint.txt' , '12345')

        >>> with open('checkpoint.txt' , 'r') as f:
        >>>    f.read()
        '12345'

    """
    with open(filename, "w", encoding="UTF-8") as f:
        f.write(content)

def save_to_pickle(treemap, filename):
    """
    Save Treemap to the 'filename' in Pickle format.

    In:
        treemap
        filename
    """
    create_storage(os.path.dirname(os.path.abspath(filename)))

    with open(filename, "wb") as f:
        pickle.dump(treemap, f)


def load_from_pickle(filename):
    """
    Load Treemap from the file 'filename'. File must be in Pickle format.

    In:
        filename
    Out:
        sorteddict
    """
    with open(filename, "rb") as f:
        obj = pickle.load(f, encoding="UTF-8")
        return obj

    return None


def proper( s: str ) -> str:
    """
    Make string Proper case. First char is upper-case, rest - lower.

    Args:
        s (str): source string

    Returns:
        (str)   Proper-cased string

    ::

        >>> import Scrapper_Helpers
        >>> Scrapper_Helpers.proper( 'jazz' )
        'Jazz'

    """
    if len(s) == 0:
        return s
    elif len(s) == 1:
        return s[0].upper()
    else:
        return s[0].upper() + s[1:].lower()


def deduplicate( s: str, char: str='_' ) -> str:
    """
    Replace duplicated chars from string.

    Args:
        s (str):    source string
        char (str): duplicated char which need deduplicate

    Returns:
        (str)   deduplicated string
    ::
    
        >>> Scrapper_Helpers.deduplicate( "abc__def" )
        'abc_def'

        >>> Scrapper_Helpers.deduplicate( "abc_def" )
        'abc_def'
    
        >>> Scrapper_Helpers.deduplicate( "abc_____def")
        'abc_def'

        >>> Scrapper_Helpers.deduplicate( "abc     def", ' ')
        'abc def'

    """
    dup = char + char

    while dup in s:
        s = s.replace(dup, char)

    return s

def get_number( s: str ) -> str:
    """
    Return numrical part from string.

    Args:
        s (str): source string

    Returns:
        (str)   heading string with numbers only
    ::

        >>> Scrapper_Helpers.get_number( '1a' )
        '1'
        
        >>> Scrapper_Helpers.get_number( '10a' )
        '10'

    """
    result = ""
    
    for c in s:
        if c.isnumeric():
            result += c
        else:
            break
            
    return result
    

def convert_to_alnum( s: str, replace_char: str="_" ) -> str:
    """
    Remove from string `s` all non-alpha-numerical symbols.

    Args:
        s (str):        source strinr
        replace_char:   char instead non-alpha-numerical symbol

    Returns:
        (str) new string

    ::

        >>> Scrapper_Helpers.convert_to_alnum( '#: {{syn|en|felid}}' )
        '_____syn_en_felid__'

    """
    return "".join( (c if c.isalnum() else replace_char for c in s ) )


def get_lognest_word( lst: list ) -> str:
    """
    Return word with maximal length.

    Args:
        lst (lsit): list with words

    Returns:
        (str)  word

    ::

        a = ['', 'syn', 'en', 'felid', '']
        >>> Scrapper_Helpers.get_lognest_word( a )
        'felid'

    """
    longest = ""
    maxlen = 0

    for w in lst:
        if len(w) > maxlen:
            maxlen = len(w)
            longest = w

    return longest


def remove_comments( s:str, startpos:int=0) -> str:
    """
    Remove HTML comments from string.

    Args:
        s (str):        source string
        startpos(int):  start position

    Returns:
        (str)   New string without comments

    ::

        >>> Scrapper_Helpers.remove_comments( '<!-- The comment -->Clean text' )
        'Clean text'

    """
    cs = s.find("<!--", startpos)
    
    if cs != -1:
        ce = s.find("-->", cs+len("<!--"))
        
        if ce != -1:
            cleaned = s[:cs] + s[ce+len("-->"):]
            return remove_comments(cleaned)
    
    return s


def extract_from_link( s:str, startpos:int =0) -> str:
    """
    Extract string from [[...]]] square brackets.

    Args:
        s (str):            source string
        startpos (int):     start position

    Returns:
        (str) New string with clean text.

    ::

        >>> Scrapper_Helpers.extract_from_link( '# An animal of the family [[Felidae]]:' )
        '# An animal of the family Felidae:'

    """
    cs = s.find("[", startpos)
    
    if cs != -1:
        ce = s.find("]", cs+len("["))
        
        if ce != -1:
            cleaned = s[:cs] + s[cs+len("["):ce] + s[ce+len("]"):]
            return extract_from_link(cleaned)
    
    return s


def iterable_to_stream(iterable, buffer_size=io.DEFAULT_BUFFER_SIZE):
    """
    Lets you use an iterable (e.g. a generator) that yields bytestrings as a read-only
    input stream.

    The stream implements Python 3's newer I/O API (available in Python 2's io module).
    For efficiency, the stream is buffered.
    """
    class IterStream(io.RawIOBase):
        def __init__(self):
            self.leftover = None
        def readable(self):
            return True
        def readinto(self, b):
            try:
                l = len(b)  # We're supposed to return at most this much
                chunk = self.leftover or next(iterable)
                output, self.leftover = chunk[:l], chunk[l:]
                b[:len(output)] = output
                return len(output)
            except StopIteration:
                return 0    # indicate EOF
    return io.BufferedReader(IterStream(), buffer_size=buffer_size)



def is_ascii( s :str ) -> bool:
    """
    Primitive fast version of ASCII checker.

    Test all symbols for ASCII or not.

    Args:
        s (str): source string

    Returns:
        (bool)
            - True - all is ACSII
            - False- not all is ACSII
    """
    return all(ord(c) < 128 for c in s)


def save_to_json( obj, filename ):
    """
    Sve object `obj` to file in JSON format.

    With pretty format with indent 4 spaces.

    Args:
        obj:        object
        filename:   file name

    ::

        >>> Scrapper_Helpers.save_to_json( [1,2,3], '123.json' )
        >>> with open('123.json' , 'r') as f:
              f.read()
        '[
            1,
            2,
            3
        ]'

    """
    js = json.dumps( obj, sort_keys=False, indent=4, ensure_ascii=False )
    put_contents( filename, js )


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


def first_true(iterable, default=False, pred=None):
    """Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.

    """
    # first_true([a,b,c], x) --> a or b or c or x
    # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
    return next(filter(pred, iterable), default)


def func_name():
    """
    :return: name of caller
    """
    return sys._getframe(2).f_code.co_name
    
    

def filterWodsProblems(s: str, context=None) -> str:
    """
    Filter word. If not correct retirn None
    """

    if context is None:
        context = func_name()

    # skip None
    if s is None:
        #log.warning(("is None: [SKIP]")
        return None

    # skip single symbols
    if len(s) == 1:
        log.warning("    filter: %s: %s: len() == 1: [SKIP]", context, s)
        return None

    # skip words contains more than 3 symbol of two dots (ABBR?)
    #if s.count('.') > 3:
    #    log.warning(("    filter: %s: %s: count('.') > 3: [SKIP]", context, s)
    #    return None

    # skip words contains :
    if s.find(':') != -1:
        log.warning("    filter: %s: %s: find(':'): [SKIP]", context, s)
        return None

    # skip more than 3 spaces
    if s.count(' ') > 3:
        log.warning("    filter: %s: %s: count(' ') > 3: [SKIP]", context, s)
        return None

    # skip #
    if s.find('#') != -1:
        log.warning("    filter: %s: %s: find('#'): [SKIP]", context, s)
        return None

    return s


def clean_surrogates( s: str ) -> str:
    """
    Decode large unicode symbols (surrogates)

    Args:
        s (str): source string

    Returns:
        (str) decoded string

    ::

        >>> Scrapper_Helpers.clean_surrogates(  "This is \\ud83d\\ude4f, an emoji." )
        'This is 🙏, an emoji.'

    """
    return str(s.encode('utf-16', 'surrogatepass').decode('utf-16'))


def pprint(*args, **kwarg):
    from pprint import PrettyPrinter
    return PrettyPrinter(indent=4).pprint(*args, **kwarg)


def dict_merge( dct: dict, merge_dct: dict ):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.items():
        if (k in dct and isinstance( dct[ k ], dict )
                and isinstance( merge_dct[ k ], collections.Mapping )):
            dict_merge( dct[ k ], merge_dct[ k ] )
        else:
            dct[ k ] = merge_dct[ k ]


def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.
    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry
    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):

        @functools.wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry
