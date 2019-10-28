import os
import json
import logging
import sqlite3
import string
import logging.config
import importlib
import bs4

import requests

from Scrapper_DB import DBExecute, DBExecuteScript, DBWrite
from conjugator.Scrapper_Conjugations_Item import ConjugationsItem

DB_NAME         = "conjugations.db"
DBConjugations  = sqlite3.connect( DB_NAME )
CACHE_FOLDER    = "cached"  # folder where stored downloadad dumps
log             = logging.getLogger(__name__)

language_map = {
    "en": "english-verb",
    "fr": "french-verb",
    "es": "spanish-verb",
    "it": "italian-verb",
    "pt": "portuguese-verb",
    "ru": "russian-verb",
    "de": "german-verb",
}

if os.path.isfile( os.path.join( 'conjugator', 'logging.ini' ) ):
    logging.config.fileConfig( os.path.join( 'conjugator', 'logging.ini' ) )

log = logging.getLogger(__name__)

# init DB
DBExecuteScript( DBConjugations, ConjugationsItem.Meta.DB_INIT )


def DBDeleteLangRecords( lang ):
    """
    Remove old lang data

    Args:
        lang (str): Lang. One of: en, de, it, es, pt, fr
    """
    log.info("Deleting old '%s' records...", lang)
    return DBExecute(DBConjugations, "DELETE FROM conjugations WHERE LanguageCode = ?", lang)


class Page:
    def __init__( self ):
        self.lang = ""
        self.label = ""
        self.text = ""
        self.url = ""

    def __repr__(self):
        return "Page" + repr( (self.lang, self.label) )


def make_request( url ):
    response = requests.get( url, verify=False )

    if response.status_code == 200:
        pass

    else:
        log.error( "HTTP-Error: %s: %s", response.status_code, response.text )
        return None

    return response.text


def get_one_verb_page( lang, label ):
    conjs_url = "http://conjugator.reverso.net/conjugation-" + language_map[ lang ] + '-' + label.lower() + '.html'

    log.info( "Fetching verb: %s", conjs_url )
    conjs_text = make_request( conjs_url )

    if conjs_text is not None:
        page = Page()
        page.lang = lang
        page.label = label
        page.text = conjs_text
        page.url = conjs_url

        return page

    else:
        log.error( "Error-No-text: %s", conjs_url )


def get_all_verbs_pages( lang ):
    page = {}

    all_verbs_url = "http://cooljugator.com/" + lang + "/list/all"

    log.info( "Fetching all verbs: %s", all_verbs_url )

    html = make_request( all_verbs_url )

    soup = bs4.BeautifulSoup( html, 'html.parser' )

    for li in soup.select( 'li.item' ):
        for a in li.find_all( 'a' ):
            verb = a.text.strip()
            page = get_one_verb_page( lang, verb )
            yield page


def filterPageProblems( page: Page ) -> Page:
    return page



def scrap_one( lang: str, page: Page ) -> list:
    """
    Scrap one page.

    It load language module and scrap data from page. Then save to DB.

    Args:
        lang (str):     Language. Example: 'en'
        page (Page):    Page instance. With `label`, `text`

    Returns:
        list of WikipediaItem  - it items with scrapped info
    """
    log.info( "(%s, %s)", lang, page )

    lm = importlib.import_module("conjugator." + lang)

    try:
        items = lm.scrap( page )

    except json.decoder.JSONDecodeError as e:
        log.error( "(%s): HTTP-response: parse error: ", page.label, exc_info=1 )
        return []

    item: ConjugationsItem
    for item in items:
        try:
            DBWrite( DBConjugations, item )
        except sqlite3.IntegrityError:
            log.warning( "PK: not unique: %s", item.PK )
            pass

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
    result = DBDeleteLangRecords( lang )
    reader = filter( filterPageProblems, get_all_verbs_pages( lang ) )

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
            scrap_one( lang, page )


