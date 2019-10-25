"""
Scrapper send 'title' to API and get clean HTML.
then HTML -> text.
then text  -> sentences.
then clean: remove [1], [2]
"""

import json
import os
import logging
import logging.config
import sqlite3
import bz2
import importlib
import string
import Scrapper_WikitextParser
from Scrapper_DB import DBExecute, DBExecuteScript, DBWrite
from Scrapper_Helpers import create_storage, is_ascii, is_lang
from wikipedia.Scrapper_Wikipedia_Item import WikipediaItem

DB_NAME         = "wikipedia.db"
DBWikipedia     = sqlite3.connect(DB_NAME, isolation_level=None)
CACHE_FOLDER    = "cached"  # folder where stored downloadad dumps
log             = logging.getLogger(__name__)
english_table   = str.maketrans( dict.fromkeys( string.punctuation ) )
ASCII           = set(string.printable)

if os.path.isfile( os.path.join( 'wikipedia', 'logging.ini' ) ):
    logging.config.fileConfig( os.path.join( 'wikipedia', 'logging.ini' ) )


# init DB
DBExecute( DBWikipedia, "PRAGMA journal_mode = OFF" )
DBExecuteScript( DBWikipedia, WikipediaItem.Meta.DB_INIT )


def DBDeleteLangRecords( lang ):
    """
    Remove old lang data

    Args:
        lang (str): Lang. One of: en, de, it, es, pt, fr
    """
    log.info("Deleting old '%s' records...", lang)
    return DBExecute(DBWikipedia, "DELETE FROM wikipedia WHERE LanguageCode = ?", lang)


def filterPageProblems( page: "Page" ):
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
    if page.text[:100].upper().find("#REDIRECT ") != -1:
        spos = page.text.upper().find( "#REDIRECT " ) + len( "#REDIRECT " )
        epos = page.text.upper().find( '\n', spos )
        if epos != -1:
            label_to = page.text[spos:epos]
        else:
            label_to = page.text[spos:]

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

    # skip non lang
    if is_lang( page.label, page.lang ) is False:
        log.warning("  filter: '%s;: some symbols not in '%s' alphabet: [SKIP]", page.label, page.lang)
        return None

    return page


class Page:
    """
    Class to hold page data: raw-text, label, lexemes, explanations, table-of-contents, text-by-raw
    """
    def __init__(self, id_, ns, label, text, lang):
        self.id_   = id_
        self.ns    = ns
        self.label = label
        self.lang = lang

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
        lexems = Scrapper_WikitextParser.parse( self.text )

        return lexems


    def __repr__(self):
        return "("+self.label+")"


class Dump:
    def __init__(self, lang):
        """
        Create dump processor instance.

        Args:
            lang (str): Lang.
        """
        self.lang = lang
        #self.url =  "https://dumps.wikimedia.org/" + lang + "wiki/20191020/" + lang + "wiki-20191020-pages-articles.xml.bz2"
        self.url =  "https://dumps.wikimedia.org/" + lang + "wiki/latest/" + lang + "wiki-latest-pages-articles.xml.bz2"

        create_storage(CACHE_FOLDER)
        self.path = os.path.join(CACHE_FOLDER, lang + "wiki-latest-pages-articles.xml.bz2")


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
            yield from XmlStreamReader( self.lang, xml_stream )


def XmlStreamReader( lang, infile ):
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

            yield Page(id_, ns, label, text, lang)

            elem.clear()




def scrap_one( lang: str, page: Page ):
    """
    Scrap one page.

    It load language module and scrap data from page. Then save to DB.

    Args:
        lang (str):     Language. Example: 'en'
        page (Page):    Page instance.

    Returns:
        list of WikipediaItem  - it items with scrapped info
    """
    log.info( "(%s, %s)", lang, page )

    lm = importlib.import_module("wikipedia." + lang)

    try:
        items = lm.scrap( page )

    except json.decoder.JSONDecodeError as e:
        log.error( "(%s): HTTP-response: parse error: ", page.label, exc_info=1 )
        return []

    item: WikipediaItem
    for item in items:
        #item.dump()
        DBWrite( DBWikipedia, item )

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

    :param lang:        str     The language code. One of: 'en', 'it', 'fr', 'de', 'pt', 'ru', 'es'. See also: Wikipedia languages.
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
