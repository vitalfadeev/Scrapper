from typing import List

from Scrapper_WikitextParser import Header
from wikipedia import Scrapper_Wikipedia
from wikipedia.Scrapper_Wikipedia_Item import WikipediaItem
from wikipedia.en.Scrapper_Wikipedia_EN_TableOfContents import Section, Root, Lang, PartOfSpeech, section_map
from wikipedia.en.Scrapper_Wikipedia_EN_Sections import LANG_SECTIONS_INDEX, PART_OF_SPEECH_SECTIONS_INDEX, VALUED_SECTIONS_INDEX


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


def scrap( page: Scrapper_Wikipedia.Page ) -> List[WikipediaItem]:
    items = []

    lexems = page.to_lexems()
    page.lexems = lexems

    # make table-of-contents (toc)
    toc = make_table_of_contents( lexems )
    page.toc = toc

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


