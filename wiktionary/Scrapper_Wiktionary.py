"""
Main Wiktionary module.

The Goal: read dump, get pages, parse, find words, save to database

"""
import os
import logging
import logging.config
import sqlite3
import bz2
import importlib
import string
from Scrapper_DB import DBExecute, DBExecuteScript, DBWrite
from . import Scrapper_Wiktionary_WikitextParser
from . Scrapper_Wiktionary_Item import WikictionaryItem
from wiktionary import Scrapper_Wiktionary_RemoteAPI

DB_NAME         = "wiktionary.db"
DBWikictionary  = sqlite3.connect(DB_NAME, isolation_level=None)
CACHE_FOLDER    = "cached"  # folder where stored downloadad dumps
log             = logging.getLogger(__name__)
english_table   = str.maketrans( dict.fromkeys( string.punctuation ) )
ASCII           = set(string.printable)

if os.path.isfile( os.path.join( 'wiktionary', 'logging.ini' ) ):
    logging.config.fileConfig( os.path.join( 'wiktionary', 'logging.ini' ) )


# init DB
DBExecute( DBWikictionary, "PRAGMA journal_mode = OFF" )
DBExecuteScript( DBWikictionary, WikictionaryItem.Meta.DB_INIT )


def create_storage(folder_name: str):
    """
    Create folders recusively.
    All folders in path created recursively.

    Args:
        folder_name (str):  Storage folder name

    ::

        create_storage("./cached")
    """
    if (not os.path.exists(folder_name)):
        os.makedirs(folder_name, exist_ok=True)


class Page:
    """
    Class to hold page data: raw-text, label, lexemes, explanations, table-of-contents, text-by-raw
    """
    def __init__(self, id_, ns, label, text):
        self.id_   = id_
        self.ns    = ns
        self.label = label

        # prepare text
        # remove BOM
        if text and text.startswith('\uFEFF'):
            text = text[1:]

        # add lead \n
        # for detection header at begin of file: '\n=='
        text = "\n" + text + "\n"
        self.text  = text

        #
        self.lexems = []
        self.toc = None
        self.explanations = []
        self.text_by_raw = {}
        self.explanation_by_sense = {}


    def to_lexems( self ) -> list:
        """
        Prepare extracted text. Make object representation of article: ==English== -> Header(English), {{en-noun}} -> Template(en-noun)

        Returns:
            (list)
        """
        # parse
        lexems = Scrapper_Wiktionary_WikitextParser.parse(self.text)

        return lexems


    def __repr__(self):
        return "("+self.label+")"


def isEnglish( s ):
    """
    Return True if `s` contains only English symbols.

    It uses for filter non-English pages in 'en' Wiktionary.

    Args:
        s (str):    String for test

    Returns:
        (bool)
            - True: `s` is English
            - False `s` is not English

    """
    return s.translate( english_table ).isalnum()


def is_ascii( s ):
    """
    Return True if `s` contains only ASCII symbols.

    Args:
        s (str):    String for test

    Returns:
        (bool)
            - True: `s` is ASCII
            - False `s` is not ASCII

    """
    for c in s:
        if c not in ASCII:
            return False

    return True


def filterPageProblems(page: Page):
    """
    Filter page. If not correct return None.

    Write record in log.

    Rules:

    - skip None
    - skip special namespaces. keep terms only
    - skip #REDIRECT
    - skip words contains :
    - skip more than 3 spaces
    - skip #
    - skip non ASCII

    Args:
        page (Page):    Page instance

    Returns:
        Page | None
    """

    # skip None
    if page is None:
        # log.warn("is None: [SKIP]")
        return None

    # skip special namespaces. keep terms only
    if int(page.ns) != 0:
        log.warning("  filter: %s: ns:%s != 0: [SKIP]", page, page.ns)
        return None

    # skip #REDIRECT
    if page.text.startswith("#REDIRECT "):
        label_to = page.text[len("#REDIRECT "):]
        log.warning("REDIRECT %s -> %s... [SKIP]", page.label, label_to)
        return None

    # skip single symbols
    # if len(page.label) == 1:
    #     log.warning("  filter: %s: len() == 1: [SKIP]", page)
    #     return None

    # skip words contains more than 3 symbol of two dots (ABBR?)
    # if page.label.count('.') > 3:
    #    log.warn("  filter: %s: count('.') > 3: [SKIP]", page.label)
    #    return None

    # skip words contains :
    if page.label.find(':') != -1:
        log.warning("  filter: %s: find(':'): [SKIP]", page.label)
        return None

    # skip more than 3 spaces
    if page.label.count(' ') > 3:
        log.warning("  filter: %s: count(' ') > 3: [SKIP]", page.label)
        return None

    # skip #
    if page.label.find('#') != -1:
        log.warning("  filter: %s: find('#'): [SKIP]", page.label)
        return None

    # skip non ASCII
    if is_ascii( page.label ) is False:
        log.warning("  filter: %s: non ASCII: [SKIP]", page.label)
        return None

    return page


def DBDeleteLangRecords( lang ):
    """
    Remove old lang data

    Args:
        lang (str): Lang. One of: en, de, it, es, pt, fr
    """
    log.info("Deleting old '%s' records...", lang)
    return DBExecute(DBWikictionary, "DELETE FROM wiktionary WHERE LanguageCode = ?", lang)


class Dump:
    def __init__(self, lang):
        """
        Create dump processor instance.

        Args:
            lang (str): Lang.
        """
        self.lang = lang
        self.url = "https://dumps.wikimedia.org/" + lang + "wiktionary/latest/" + lang + "wiktionary-latest-pages-articles.xml.bz2"
        create_storage(CACHE_FOLDER)
        self.path = os.path.join(CACHE_FOLDER, lang + "wiktionary-latest-pages-articles.xml.bz2")


    def download(self):
        """
        Download dump

        ::

            Dump('en').download()

        """
        url = self.url
        dest = self.path

        if os.path.isfile(dest):
            pass
        else:
            from Scrapper_Downloader import download
            log.info( "Downloading: %s", url )
            download( url, dest )

        return self


    def getReader(self):
        """
        Return reader. Read .xml.bz2 dump and return pages. See also: XmlStreamReader

        ::

            reader = Dump(lang).download().getReader()
            for page in reader:
                scrap_one( lang, page )

        """
        with bz2.open(self.path, "r") as xml_stream:
            yield from XmlStreamReader(xml_stream)


def XmlStreamReader( infile ):
    """
    Create reader for read `infile ` stream and return `Page()` objects.

    Args:
        infile (file): Stream

    Returns:
        Iterator[ Page ]
    """
    from lxml import etree

    context = etree.iterparse(infile, huge_tree=True, events=('start', 'end'))

    # read xmlns
    for event, elem in context:
        if event == "start" and etree.QName(elem).localname == "mediawiki":
            xmlns = elem.nsmap[elem.prefix]
            page_tag     = "{"+xmlns+"}"+"page"
            id_tag       = "{"+xmlns+"}"+"id"
            ns_tag       = "{"+xmlns+"}"+"ns"
            title_tag    = "{"+xmlns+"}"+"title"
            revision_tag = "{"+xmlns+"}"+"revision"
            text_tag     = "{"+xmlns+"}"+"text"
            break

    # read pages
    for event, elem in context:
        if event == "end" and elem.tag == page_tag:
            page     = elem

            id_      = page.findtext(id_tag      , default='')    # page/id
            ns       = page.findtext(ns_tag      , default='')    # page/bs
            label    = page.findtext(title_tag   , default='')    # page/title
            revision = page.find(revision_tag)                    # page/revision
            text     = revision.findtext(text_tag, default='')    # page/text

            yield Page(id_, ns, label, text)

            elem.clear()


def convert_explanation_raw_to_text( label, explanation_text ):
    """
    It send `explanation_text` and `label` to Wiktionary API. Then parse response, and return plain human-readable text.

    It make HTTP request via `Scrapper_Wiktionary_RemoteAPI`.

    Args:
        label (str):            Wiktionary page title. Example: 'cat'
        explanation_text (str): raw-text. Example: {{en-noun|s}}

    Returns:
        Readable text. Example: 'cat (plural: cats)'

    """
    label = label

    html = Scrapper_Wiktionary_RemoteAPI.parse( label, explanation_text )
    lexems = Scrapper_Wiktionary_WikitextParser.parse( html )

    text = "".join( l.to_text() for l in lexems )

    return text


def scrap_one(lang, page):
    """
    Scrap one page.

    It load language module and scrap data from page. Then save to DB.

    Args:
        lang (str):     Language. Example: 'en'
        page (Page):    Page instance.

    Returns:
        list of WiktionaryItem  - it items with scrapped info
    """
    log.info( "(%s, %s)", lang, page )

    lm    = importlib.import_module("wiktionary." + lang)
    items = lm.scrap( page )

    item: WikictionaryItem
    for item in items:
        item.dump()
        DBWrite( DBWikictionary, item )

    return items


def scrap_one_wrapper(args):
    """
    It used with multiprocessing. Because multiprocessing callback pass arguments as tuple. This wrapper help expand tuple.

    it call `scrap_one()` with `args`.

    Args:
        args (tuple):  Args
    """
    try:
        scrap_one( *args )
    except Exception as e:
        log.error( "  %s", args, exc_info=True )


def scrap( lang: str ="en", workers: int = 1 ):
    """
    The main function in Scrapper.
    Here run multiprocessing, create .bz2 reader, read dump, read pages.

    :param lang:        str     The language code. One of: 'en', 'it', 'fr', 'de', 'pt', 'ru', 'es'. See also: Wiktionary languages.
    :param workers:     int     Number of workers in multiprocessing. If workers=1, then run in single process.
                                Recommendation: workers = 10 (for parallel network requests)
    """
    result = DBDeleteLangRecords( lang )
    reader = filter( filterPageProblems, Dump(lang).download().getReader() )

    if workers > 1:
        import multiprocessing
        import itertools

        pool = multiprocessing.Pool( workers )
        for result in pool.imap( scrap_one_wrapper, zip( itertools.repeat( lang ), reader ) ):
            pass
        pool.close()
        pool.join()

    else: # single process
        for page in reader:
            log.warning( page )
            scrap_one( lang, page )

