from typing import List
import nltk
import re
import string
import logging
from bs4 import BeautifulSoup
from Scrapper_Helpers import deduplicate, convert_to_alnum, proper, get_lognest_word, is_ascii, unique
from Scrapper_WikitextParser import Header, Link, Template, parse, String, Li, Dl, Container
from wikipedia import Scrapper_Wikipedia
from wikipedia import Scrapper_Wikipedia_RemoteAPI
from wikipedia.Scrapper_Wikipedia_Item import WikipediaItem

nltk.download( 'punkt' )
from nltk import tokenize

log = logging.getLogger(__name__)

see_also_titles_by_lang = {
    'en': ['see also'],
    'fr': ['voir aussi'],
    'de': [],
    'it': ['guarda anche', 'voci correlate'],
    'es': ['véase también'],
    'pt': ['ver também'],
    'ru': ['cм. также', 'cмотри также'],
}


def get_label_type( expl ):
    """
    Return LabelType for item.

    Args:
        expl (Explanation):         Explanation
        item (WikictionaryItem):    WikictionaryItem

    Returns:
        (str)   LabelType

    ::

        LabelType for 'cat' for explanation
            ## A domesticated [[subspecies]] (''[[Felis silvestris catus]]'') of [[feline]] animal, commonly kept as a house [[pet]]. {{defdate|from 8<sup>th</sup>c.}}
        is:
            "Noun_DEFDATE_Subspecies_Silvestris_Feline"

    """
    # wt = proper(item.Type) if item.Type is not None else ""

    # Extract the list of item enclosed in {{ }}
    # For each item found , if there is | inside , then split and take only longest word
    # Convert all non 0-9 A-Z into _
    # Deduplicate _ _ into single _
    # Make all words in upper case
    list1 = []
    for t in expl.find_objects(Template, recursive=True, exclude=[li for li in expl.find_objects((Li, Dl))]):
        inner = t.raw
        s = convert_to_alnum(inner , '_')
        s = deduplicate(s, '_')
        s = s.strip('_')
        words = []
        for ws in s.split("|"):
            for w in ws.split('_'):
                words += w.split(' ')
        s = get_lognest_word(words)
        s = s.upper()
        list1.append(s)

    # Extract the list of item enclosed in [[ ]]
    # For each item found , if there is | inside , then split and take only longest word
    # Convert all non 0-9 A-Z into _
    # Deduplicate _ _ into single _
    # Make all words with first letter uppercase and others lower case (propercase)
    list2 = []
    for l in expl.find_objects(Link, recursive=True, exclude=[li for li in expl.find_objects((Li, Dl))]):
        s = l.get_text()
        s = convert_to_alnum(s, '_')
        s = deduplicate(s, '_')
        s = s.strip('_')
        words = []
        for ws in s.split('_'):
            for w in ws.split(' '):
                words.append(w)
        s = get_lognest_word(words)
        s = proper(s)
        list2.append(s)

    # remove all [ ( { ) ] } from the line, and extract all words separated by spaces
    # keep only words having a lenght>=3
    # Convert all non 0-9 A-Z into _
    # Deduplicate _ _ into single _
    # Make all words in lowercase
    list3 = []
    words = []
    for w in expl.find_objects(String, recursive=False, exclude=[li for li in expl.find_objects((Li, Dl))]):
        words.append(w.get_text())

    s = " ".join(words)
    s = s.replace('(', ' ').replace(')', ' ')
    s = deduplicate(s, ' ')
    s = convert_to_alnum(s)
    s = deduplicate(s, '_')
    s = s.strip('_')

    words = []
    for ws in s.split('_'):
        for w in ws.split(' '):
            words.append(w)
    list3 = [w.lower() for w in words if len(w) >= 3]

    # Add TYPE + (the 4 first items of the concatenated list :  list1 + List2 + list3
    # Concat
    biglst = list1 + list2 + list3

    return "_".join(biglst[:4])


def get_page( lang, title ):
    # https://en.wikipedia.org/wiki/Special:ApiSandbox
    # https://en.wikipedia.org
    #   /w/api.php?action=parse&format=json&page=Cat&prop=text%7Ccategories%7Clinks%7Cexternallinks%7Csections%7Cdisplaytitle%7Ciwlinks%7Cproperties%7Cparsewarnings&disablelimitreport=1&disableeditsection=1&disablestylededuplication=1&utf8=1
    js = Scrapper_Wikipedia_RemoteAPI.parse_page( title )

    # js["parse"]["title"]
    # js["parse"]["pageid"]
    # js["parse"]["text"]["*"]
    #
    # js["links"]["ns"]
    # js["links"]["*"]
    # js["iwlinks"]["prefix"]
    # js["iwlinks"]["url"]
    # js["iwlinks"]["*"]
    # js["displaytitle"]
    # js["sections"]
    # js["sections"]["toclevel"]
    # js["sections"]["level"]
    # js["sections"]["line"]
    # js["sections"]["number"]
    # js["sections"]["index"]
    # js["sections"]["fromtitle"]
    # js["sections"]["byteoffset"]
    # js["sections"]["anchor"]
    # js["externallinks"]
    # js["categories"]["ns"]
    # js["categories"]["*"]

    return js


def find_text_in_brackets( text, op='(', cl=')' ):
    """
    Find text between matched brackets.

    Args:
        text (str): text
        op (str):   open bracket symbol
        cl (str):   close bracket symbol

    Returns:
        (tuple(start, end))  Return tuple with start position where found open bracket `op`, and positions where found matched close bracket `cl`.

    ::

        >>> find_text_in_brackets( "123(45)", '(', ')' )
        (3, 6)

    """
    spos = None
    epos = None

    opened = 0
    closed = 0

    for i, c in enumerate( text ):
        if c == op:
            opened += 1

            if spos is None:
                spos = i

        elif c == cl:
            closed += 1

            if opened == closed:
                epos = i
                break

    return (spos, epos)


def replace_text_in_brackets( text, replace_wuth, op='(', cl=')' ):
    """
    Find first occurence `(...)` in text and replace to `replace_wuth`. Or remove if `replace_wuth` == ''

    Args:
        text (str):         text
        replace_wuth (str): replace text
        op (str):           open bracket sumbol
        cl (str):           close bracket symbol

    Returns:
        (str) new string with replacement
    """
    result = text

    (spos, epos) = find_text_in_brackets( text, op, cl )

    if spos and epos:
        result = text[:spos] + replace_wuth + text[epos+1:]

    return result


def get_explaination_from_api( js, html, soup ):
    # 1. find
    # <div class="mw-parser-output">
    #   p, p, p, ...
    #     skip: <p class="mw-empty-elt">
    #   <div id ="toc">
    # 2. remove [1]. [2], ...
    # 3. remove pronunciation
    #    (/.../) <- between round brackets (), between slashes //, in first  explanation: (/ ... /)
    explainations = []

    for main_container in soup.select( ".mw-parser-output" ):
        for child in main_container.findChildren( recursive=False ):
            # p
            if child.name == 'p' and ( len( child.attrs.get("class", []) ) == 0 ):
                text = child.text
                # 2. remove [1]. [2], ...
                cleaned = re.sub( '\[[0-9]+\]', '', text )
                # 3. remove pronunciation (/...)
                if cleaned.find( '(/' ) != -1:
                    cleaned = replace_text_in_brackets( cleaned, '', op='(', cl=')' )
                explainations.append( cleaned )

            # TOC -> stop
            if child.name == 'div' and ("toc" in child.attrs.get("class", []) ):
                break

    return explainations


def get_all_wikipedia_links_from_api( js, html, soup ):
    links = []

    for link in js["parse"]["links"]:
        ns = int( link["ns"] )
        if ns == 0:
            links.append( link["*"] )

    return links


def get_all_wiktionary_links_from_api( js, html, soup ):
    links = []

    # js["iwlinks"]["prefix"]
    # js["iwlinks"]["url"]
    # js["iwlinks"]["*"]
    for link in js["parse"]["iwlinks"]:
        prefix = link["prefix"]
        if prefix in ["wikt", "wiktionary"]:
            path = link["*"]
            cleaned = re.sub( '^wikt:', '', path )
            cleaned = re.sub( '^wiktionary:', '', cleaned )
            links.append( cleaned )

    return links


def get_all_wikidata_links_from_api( js, html, soup ):
    links = []

    # js["iwlinks"]["prefix"]
    # js["iwlinks"]["url"]
    # js["iwlinks"]["*"]
    for link in js["parse"]["iwlinks"]:
        prefix = link["prefix"]
        if prefix in ["wikidata"]:
            path = link["*"]
            cleaned = re.sub( '^wikidata:', '', path )
            links.append( cleaned )

    return links


def get_all_links_from_see_also_from_api( js, html, soup, section_titles ):
    # 1. find 'see also'. h1, h2, h3, h4, h5
    # 2. find all <a>.
    # 3. until EOF | other h1, h2, h3, h4, h5: with higher level

    links = []

    # 1. find 'see also'. h1, h2, h3, h4, h5
    iterator = soup.find_all( recursive=True )

    for header in iterator:
        if header.name in ["h1", "h2", "h3", "h4", "h5"]:
            # header found
            if header.text.lower() in section_titles:
                # 2. find all <a>.
                for e in iterator:
                    if e.name == 'a':
                        href = e.attrs.get('href', None)
                        if href:
                            if not href.startswith( '#' ):
                                links.append( href )

                    if e.name in [ "h1", "h2", "h3", "h4", "h5" ]:
                        # 3. until EOF | other h1, h2, h3, h4, h5: with higher level
                        break

    return links


def get_explanation_examples_from_api( js, html, soup, label ):
    # 1. split text to sentences
    # 2. split sentence to words
    # 3. split label to tokens: 'An American in Paris' to to ['An' 'American' 'in' 'Paris']
    # 4. find match. (ignore case)
    #      if found: OK
    # 5. remove pronunciation
    #    (/.../) <- between round brackets (), between slashes //, in first  explanation: (/ ... /)
    examples = []

    # 3. split label to tokens: 'An American in Paris' to to ['An' 'American' 'in' 'Paris']
    # here remove all non-chars - is split
    # then concat by space
    # and space around
    # example: 'The text with... 1, 2, 3' -> ['The', 'text', 'with', '1', '2', '3'] -> ' The text with 1 2 3 '
    # then can match with 'The text'
    expecteds = re.split( "\W+" , label )
    lowered = list( map( str.lower, expecteds ) )
    cleaned_expected = ' ' + ' '.join( lowered ) + ' '  # is pattern for search

    # 1. split text to sentences
    for i, p in enumerate( soup.select( 'p' ) ):
        text = p.text

        # remove prunounciation: (/...)
        # in 1-2 paragraph
        if i <= 2 and text.find( '(/' ) != -1:
            text = replace_text_in_brackets( text, '', op='(', cl=')' )

        # to senteces
        sentences = tokenize.sent_tokenize( text )

        for sentence in sentences:
            # lower
            lowered = sentence.lower()
            # remove [1]. [2], ...
            cleaned = re.sub( '\[[0-9]+\]', '', lowered )
            # 2. split sentence to words
            words = re.split( "\W+" , cleaned )
            # to string
            cleaned_sentence = ' ' + ' '.join( words ) + ' '

            # 4. match
            # [ 'An' 'American' 'in' 'Paris' ] -> 'An American in Paris'
            if cleaned_expected in cleaned_sentence:
                examples.append( sentence )

    return examples


def get_explanatoin_lexems( page ):
    raw = page.text

    blocks = []

    # parse raw
    lexemes = parse( raw )

    # find text blocks before Header
    for lexem in lexemes:
        if isinstance( lexem, Header ):
            break

        blocks.append( lexem )

    return blocks


def get_label_type_from_api( js, html, soup, explanations_lexems ):
    # 1. parse part of text : explanations only
    # 2. Text block at page start. Until ==Header==. Is explanation.

    # build LabelType
    expl = Container()
    expl.childs = explanations_lexems

    return get_label_type( expl )


def scrap( page: Scrapper_Wikipedia.Page ) -> List[WikipediaItem]:
    """
    Scrap page.

    - 1 Take page title `page.label`
    - 2. Send to Wikipedia API
    - 3. Get HTML
    - 4. Parse HTML with BeautifulSoup
    - 5. Get gems: Explanations, Links, Examples, ....
    - 6. Generate LabelType, PrymaryKey
    - 7. Return `items` to parent script


    Args:
        page (Page):  instace of Page. It contain `label` `text`, `id_`, `ns` fetched from dump.

    Returns:
        (list)  List of items.
    """
    # - 1 Take page title `page.label`
    lang = page.lang
    title = page.label
    #title = 'AbalonE'

    Scrapper_Wikipedia_RemoteAPI.DOMAIN = "https://{}.wikipedia.org".format( lang )

    # - 2. Send to Wikipedia API
    # - 3. Get HTML
    js = get_page( lang, title )

    html = js["parse"]["text"]["*"]

    # - 4. Parse HTML with BeautifulSoup
    soup = BeautifulSoup( html, 'html.parser' )

    # - 5. Get gems: Explanations, Links, Examples, ....
    items = []  # scrapped data container

    # get explanation lexems. for to use with LabelType builder
    explanation_lexems = get_explanatoin_lexems( page )

    #
    item = WikipediaItem()

    # Label Name
    item.LabelName = page.label
    item.LanguageCode = lang

    item.ExplainationWPRaw = "".join( l.raw for l in explanation_lexems )  # join lexems for get one raw text
    item.ExplainationWPTxt = "\n".join( get_explaination_from_api( js, html, soup ) )  # join text blocks. from soup we taken <p> - 1~5 blockss

    # Description Links
    item.DescriptionWikipediaLinks = unique(                        # unique
        filter(
            lambda s: s != title,                                   # skip self
            get_all_wikipedia_links_from_api( js, html, soup )      # get WP links
        )
    )
    item.DescriptionWiktionaryLinks = unique(                       # unique
        filter(
            lambda s: s != title,                                   # skip self
            get_all_wiktionary_links_from_api( js, html, soup )     # get WT links
        )
    )
    item.DescriptionWikidataLinks = unique(                         # unique
        filter(
            lambda s: s != title,                                   # skip self
            get_all_wikidata_links_from_api( js, html, soup )       # get WD links
        )
    )

    # Self Url
    item.SelfUrlWikipedia = "https://" + lang + ".wikipedia.org/wiki/" + page.label   # check in dump

    # SeeAlso
    item.SeeAlso = get_all_links_from_see_also_from_api( js, html, soup, see_also_titles_by_lang[ lang ] )
    item.SeeAlsoWikipediaLinks = unique(                                            # unique
        filter(
            lambda s: s != title,                                                   # skip self
            [ l[len('/wiki/'):] for l in item.SeeAlso if l.startswith('/wiki/') ]   # keep WP links only: /wiki/...
        )
    )
    item.SeeAlsoWiktionaryLinks = unique(                                           # unique
        filter(
            lambda s: s != title,                                                   # skip self
            [ re.sub( 'https://[\w]+.wiktionary.org/wiki/', '', l ) for l in item.SeeAlso if l.find(".wiktionary.org/") != -1 ]  # keep WKT links only: https://en.wiktionary.org/wiki/...
        )
    )

    # Examples
    # item.ExplainationExamplesRaw = get_all_explanation_examples_raw( page, toc )
    item.ExplainationExamplesTxt = get_explanation_examples_from_api( js, html, soup, title )

    # - 6. Generate LabelType, PrymaryKey
    # LabelType
    item.LabelTypeWP = get_label_type_from_api( js, html, soup, explanation_lexems )

    # PrimaryKey
    item.PK = item.LanguageCode + "-" + item.LabelName + "§" + item.LabelTypeWP + "-" + str( page.id_ )

    items.append( item )

    # - 7. Return `items` to parent script
    return items
