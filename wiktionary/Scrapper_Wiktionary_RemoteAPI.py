from functools import lru_cache
import requests
import logging
import logging.config
from bs4 import BeautifulSoup
from Scrapper_Helpers import retry

DOMAIN  = "https://en.wiktionary.org"
API_URL = "/w/api.php"
log     = logging.getLogger(__name__)


def set_domain( lang: str ):
    DOMAIN = "https://{}.wiktionary.org".format( lang )


@lru_cache(maxsize=32)
def parse( title, text ):
    # wiki-text wrapped by xml
    params = {
        "action"                   : "parse",
        "format"                   : "json",
        "title"                    : title,
        "text"                     : text,
        "prop"                     : "text",
        "disablelimitreport"       : "1",
        "disableeditsection"       : "1",
        "disablestylededuplication": "1",
        "utf8"                     : "1",
    }

    response = _post(params)

    if response.status_code == 200:
        data = response.json()
        return data['parse']['text']['*']
    else:
        log.error( '  response.status_code: %s', response.status_code )
        log.error( '  response.text: %s', response.text )


def expand_templates( title: str, raws: list ) -> list:
    to_send = []
    result = []

    # prepare text. wrap with <span>
    for i, raw in enumerate( raws ):
        # wrap with <div>
        s = raw if raw else ''
        to_send.append( "<span class=\"data-ixioo-id\" id=\"" + str(i) + "\">" + s + "</span>" )

    text = "<span>" + "\n" + "\n".join( to_send ) + "\n" + "</span>"

    # make request
    parsed_text = parse( title, text )

    # parse response
    from bs4 import BeautifulSoup

    soup = BeautifulSoup( parsed_text, 'lxml' )

    # fetch id
    txts = []
    for e in soup.find_all( 'span', class_="data-ixioo-id" ):
        id_ = e.get( 'id' )
        txts.append( e.text )

    return txts


@lru_cache(maxsize=32)
def get_wikitext( title=None ):
    # wiki-text wrapped by xml
    params = {
        "action"      : "query",
        "format"      : "json",
        "export"      : "1",
        "exportnowrap": "1",
        "titles"      : title,
        "utf8"        : "1"
    }

    response = _post(params)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        if soup.body.mediawiki.page is not None:
            # page found
            text = soup.body.mediawiki.page.revision.text
            return text

        else:
            # no page in DB
            # soup.body.mediawiki.page is None
            log.error( '  no page: %s', title )

    else:
        log.error( '  response.status_code: %s', response.status_code )
        log.error( '  response.text: %s', response.text )


@retry((requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.HTTPError), tries=5, delay=1)
def _get( params ):
    url = DOMAIN + API_URL
    action = params.get('action', '')
    titles = params.get('titles', params.get('title', ''))
    log.debug( "  Request to: %s: %s(%s)", url, action, titles )
    response = requests.get(url, params=params, timeout=(15, 27))
    return response


@retry((requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.exceptions.HTTPError), tries=5, delay=1)
def _post( params ):
    url = DOMAIN + API_URL
    action = params.get('action', '')
    titles = params.get('titles', params.get('title', ''))
    log.debug( "  Request to: %s: %s(%s)", url, action, titles )
    response = requests.post(url, data=params, timeout=(15, 27))
    return response


