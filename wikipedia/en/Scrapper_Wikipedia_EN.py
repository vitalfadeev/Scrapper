from typing import List
import nltk
from Scrapper_Helpers import deduplicate, convert_to_alnum, proper, get_lognest_word
from Scrapper_WikitextParser import Header, Link, Template
from wikipedia import Scrapper_Wikipedia
from wikipedia.Scrapper_Wikipedia_Item import WikipediaItem
from wikipedia import Scrapper_Wikipedia_RemoteAPI
from wikipedia.en.Scrapper_Wikipedia_EN_TableOfContents import Section, Root, Lang, PartOfSpeech, section_map
from wikipedia.en.Scrapper_Wikipedia_EN_Sections import LANG_SECTIONS_INDEX, PART_OF_SPEECH_SECTIONS_INDEX, VALUED_SECTIONS_INDEX

nltk.download( 'punkt' )
from nltk import tokenize


def make_table_of_contents( lexemes: list ) -> Root:
    """
    Create Table of contents for given `lexemes`.

    it search <Header> tokens. In raw-text it '=English=', '===Noun==='. Then detect level of header. Then build tree.

    Args:
        lexemes (list):     List of lexemes. Lexemes going from raw-text parser (module Scrapper_Wiktionary_WikitextParser)

    Returns:
        (Root)  Tree root.

    ::

        # for 'cat'
        toc = make_table_of_contents( lexems )

        # result is:
        toc.dump()

        # result:
        ...

    """
    root = Root()
    last = root

    # 1. scan each lexem
    # 2. get Headers
    # 3. make tree
    # group lexems by class
    for lexem in lexemes:
        if isinstance( lexem, Header ):
            header = lexem

            # flags
            beauty_name = header.name.lower().strip()
            if header.level < 4 and beauty_name in LANG_SECTIONS_INDEX:
                # Language
                node = Lang()
                node.title = header.name
                node.title_norm = LANG_SECTIONS_INDEX[ beauty_name ]
                node.level = header.level

            elif beauty_name in PART_OF_SPEECH_SECTIONS_INDEX:
                # Part of speech
                node = PartOfSpeech()
                node.title = header.name
                node.title_norm = PART_OF_SPEECH_SECTIONS_INDEX[ beauty_name ]
                node.level = header.level

            elif beauty_name in VALUED_SECTIONS_INDEX:
                # Synonyms, Antonyms, Translations
                cls = section_map.get( beauty_name, Section )
                node = cls()
                node.title = header.name
                node.title_norm = VALUED_SECTIONS_INDEX[ beauty_name ]
                node.level = header.level

            else:
                # Any other section
                node = Section()
                node.title = header.name
                node.title_norm = beauty_name
                node.level = header.level

            # hierarchy
            if last is root:
                # top-level node
                parent = last
                parent.append(node)
                last = node

            elif header.level > last.level:
                # child node
                parent = last
                parent.append(node)
                last = node

            elif header.level == last.level:
                # same level node
                parent = last.parent
                parent.append(node)
                last = node

            else:
                # parent node
                # find parent
                parent = last

                while parent is not root:
                    if header.level > parent.level:
                        break
                    else:
                        parent = parent.parent

                parent.append(node)
                last = node

            # index by name
            parent.sections_by_name[ beauty_name ] = node

        # save lexems
        # text block
        last.lexemes.append( lexem )
        # index by class
        last.lexemes_by_class[ type( lexem ) ][ lexem.name ].append( lexem )
        for lex in lexem.find_all( recursive=True ):
            last.lexemes_by_class[ type( lex ) ][ lex.name ].append( lex )

    return root


def get_label_type( expl, item ):
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
    wt = proper(item.Type) if item.Type is not None else ""

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

    return wt + "_" + "_".join(biglst[:4])


def get_first_block_before_header( toc: Root ):
    block = []
    for lexem in toc.lexemes:
        block.append( lexem.raw )

    return block


def convert_raw_to_txt( page:Scrapper_Wikipedia.Page, raws:list ) -> list:
    txts = Scrapper_Wikipedia_RemoteAPI.expand_templates( page.label, raws )
    return txts


def get_all_wikipedia_links( page, toc ):
    links = []

    for node in toc.find_all( recursive=True ):
        links.extend( node.lexemes_by_class[ Link ][''] )

    return links


def get_all_wiktionary_links( page, toc ):
    links = [ ]

    for node in toc.find_all( recursive=True ):
        links.extend( node.lexemes_by_class[ Template ][ 'll' ] )
        links.extend( node.lexemes_by_class[ Template ][ 'link' ] )

    return links


def get_all_links_from_see_alo( page, toc ):
    links = []

    for node in toc.find_all( recursive=True ):
        if node.title_norm == 'see also':
            links.extend( node.lexemes_by_class[ Link ][''] )

    return links


def get_all_links_from_section( page, toc, section_title='see also' ):
    links = []

    for node in toc.find_all( recursive=True ):
        if node.title_norm == section_title:
            links.extend( node.lexemes_by_class[ Link ][''] )

    return links


def get_all_explanation_examples_raw( page, toc ):
    raws = []

    for lexem in page.lexems:
        raws.append( lexem.raw )

    text = "\n".join( raws )
    sentences = tokenize.sent_tokenize( text )

    return sentences


def scrap( page: Scrapper_Wikipedia.Page ) -> List[WikipediaItem]:
    items = []

    lexems = page.to_lexems()
    page.lexems = lexems

    # make table-of-contents (toc)
    toc = make_table_of_contents( lexems )
    page.toc = toc

    #
    item = WikipediaItem()

    #
    item.LabelName = page.label
    item.LabelTypeWP = get_label_type( ... )
    item.LanguageCode = "en"

    item.ExplainationWPRaw = get_first_block_before_header( toc )
    item.ExplainationWPTxt = convert_raw_to_txt( item.ExplainationWPRaw )

    item.DescriptionWikipediaLinks = get_all_wikipedia_links( page, toc )
    item.DescriptionWiktionaryLinks = get_all_wiktionary_links( page, toc )

    item.SelfUrlWikipedia = "https://en.wikipedia.org/wiki/" + page.label   # check in dump

    item.SeeAlso = get_all_links_from_see_alo( page, toc )
    item.SeeAlsoWikipediaLinks = get_all_links_from_section( page, toc , section_title='see also' )

    item.ExplainationExamplesRaw = get_all_explanation_examples_raw( page, toc )
    item.ExplainationExamplesTxt = []

    return items


# The explanation:
# - first block before TOC (before first header, like the: ==Etymology== )
#
# The sentence:
# - splitted by DOT, EOL
# - splitted by COMMA
#
# The word:
# - spaces before and after
# - cat start of EOL
# - not case-sensitive (cat = Cat)
#


