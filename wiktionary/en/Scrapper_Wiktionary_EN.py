import itertools
import collections
import string
import re
import pprint
from typing import List, Any, Iterator
from collections import defaultdict
import Scrapper_IxiooAPI
from wiktionary import Scrapper_Wiktionary
from wiktionary import Scrapper_Wiktionary_RemoteAPI
from wiktionary.Scrapper_Wiktionary_Item import WikictionaryItem
from wiktionary.Scrapper_Wiktionary_ValuableSections import VALUABLE_SECTIONS as ws
from wiktionary import Scrapper_Wiktionary_WikitextParser
from wiktionary.Scrapper_Wiktionary_WikitextParser import Section, Header, Template, Li, Dl, Link, String, Container
from wiktionary.en.Scrapper_Wiktionary_EN_Sections import LANG_SECTIONS_INDEX, PART_OF_SPEECH_SECTIONS_INDEX, VALUED_SECTIONS_INDEX, VALUED_SECTIONS
from ..Scrapper_Wiktionary_Checkers import check_node
from Scrapper_Helpers import unique, filterWodsProblems

# EN = 'en'
# DE = 'de'
# PT = 'pt'
# FR = 'fr'
# IT = 'it'
# ES = 'es'
# RU = 'ru'


class TocNode(list):
    def __init__(self, title='', level=0, parent=None):
        super().__init__()
        self.title               = title                    # title             str
        self.title_norm          = ""                       # title_normal      str
        self.level               = level                    # level             int
        self.parent              = parent                   # parent            TocNode
        self.lexems              = []                       # section lexems    Container
        self.item                = WikictionaryItem()       # store             WiktionaryItem
        self.index_in_toc        = ''
        self.index_pos           = ''
        self.is_lang             = False
        self.is_pos              = False
        self.is_valued_section   = False
        self.is_explanation      = False
        self.is_example          = False
        self.is_li               = False
        self.is_list             = False
        self.is_text             = False
        self.is_header           = False
        self.is_trans_top        = False
        self.is_explanation_root = False
        self.is_explanation_node = False
        self.is_leaf_explanation = False
        self.sense_raw           = ""
        self.sense_txt           = ""
        self.sections            = {}                       # child section. sections[ 'Synonyms' ] = node
        self.explanations        = None
        self.sense_matches       = None
        self.by_sense            = None                     # cache. .by_sense[ 'sense' ] = Container

    def append(self, node) -> None:
        node.parent = self
        super().append(node)

    def find_all(self, recursive=False) -> Iterator[ "TocNode" ]:
        for c in self:
            yield c

            if recursive:
                yield from c.find_all(recursive)


    def find_lexem(self, recursive=True) -> Iterator[ Container ]:
        # return node lexem and node lexem childs
        for lexem in self.lexems:
            yield lexem

            if recursive:
                yield from lexem.find_all( recursive )


    def find_parents( self ) -> Iterator[ "TocNode" ]:
        parent = self.parent
        while parent:
            yield parent
            parent = parent.parent


    def find_lang_section( self ) -> Iterator[ "TocNode" ]:
        yield from filter( lambda node: node.is_lang, self.find_all( recursive=True ) )


    def find_part_of_speech_section( self ) -> Iterator[ "TocNode" ]:
        yield from filter( lambda node: node.is_pos, self.find_all( recursive=True ) )


    def find_explanations( self ) -> Iterator[ "TocNode" ]:
        yield from filter( lambda node: node.is_explanation, self.find_all( recursive=True ) )


    def find_examples( self ) -> Iterator[ "TocNode" ]:
        yield from filter( lambda node: node.is_example, self.find_all( recursive=True ) )


    def get_parent_lang_node( self ) -> "TocNode":
        node = self.parent

        while node is not None:
            if node.is_lang is True:
                return node
            else:
                node = node.parent

        return None


    def get_parent_pos_node( self ) -> "TocNode":
        node = self.parent

        while node is not None:
            if node.is_pos is True:
                return node
            else:
                node = node.parent

        return None


    def merge_with_parents( self ) -> WikictionaryItem:
        """ Merge item data with parents data. Starts from parent. Ends on 'self'.
            Parents values replaced by 'self' values (- for dict, str, int, for list - append).
        """
        item = WikictionaryItem()

        for parent in reversed( list( self.find_parents() ) ):
            item.merge( parent.item )

        item.merge( self.item )

        return item


    def merge_with_childs( self ) -> WikictionaryItem:
        """ Merge item data with childs data. Starts from 'self' node. Ends on leaf.
        """
        item = WikictionaryItem()

        for child in self.find_all( recursive=True ):
            item.merge( child.item )

        item.merge( self.item )

        return item


    def dump(self, level=0, wide=False, with_lexems=False):
        WIDTH = 68

        # print header
        if level == 0:
            if wide:
                s = ""
                print(s.ljust(WIDTH), self.item.dumps(print_header=True))

            # recursive
            for i, child in enumerate(self, start=1):
                child.dump(level+1, wide, with_lexems)
            return

        # print node
        if wide:
            # wide. show item columns
            s = ("  " * level) + ' ' + self.index_in_toc + ' ' + self.title
            print(s.ljust(WIDTH) + self.item.dumps())
        else:
            # short. title only
            print("  " * level + self.index_in_toc + ' ' + repr(self))
            if with_lexems:
                for lexem in self.lexems:
                    print("  " * level + '- ' +  repr(lexem))

        # recursive
        for child in self:
            child.dump(level+1, wide, with_lexems)


    def dump_sense_raw( self, level=0 ):
        if self.sense_raw:
            print( '  '*level + self.index_in_toc + ' ' + self.sense_raw )

        # recursive
        for node in self:
            node.dump_sense_raw( level+1 )


    def dump_sense_txt( self, level=0 ):
        if self.sense_txt:
            print( '  '*level + self.index_in_toc + ' ' + self.sense_txt )

        # recursive
        for node in self:
            node.dump_sense_txt( level+1 )


    def __repr__(self):
        if self.is_lang:
            return self.title
        elif self.is_pos:
            return self.title
        elif self.is_explanation_root:
            return self.title
        elif self.is_explanation:
            return self.title
        elif self.is_example:
            return self.title
        else:
            return self.title


def make_tree( lexems: list ) -> TocNode:
    root = TocNode()
    last = root

    # 1. scan each lexem
    # 2. get Headers
    # 3. make tree
    # group lexems by class
    for lexem in lexems:
        if isinstance( lexem, Header):
            header = lexem
            node = TocNode( title=header.name, level=header.level )
            node.is_header = True
            node.lexems.append( header )

            # flags
            beauty_name = header.name.lower().strip()
            if header.level < 4 and beauty_name in LANG_SECTIONS_INDEX:
                # Language
                node.is_lang = True
                node.title_norm = LANG_SECTIONS_INDEX[ beauty_name ]

            elif beauty_name in PART_OF_SPEECH_SECTIONS_INDEX:
                # Part of speech
                node.is_pos = True
                node.title_norm = PART_OF_SPEECH_SECTIONS_INDEX[ beauty_name ]

            elif beauty_name in VALUED_SECTIONS_INDEX:
                # Synonyms, Antonyms, Translations
                node.is_valued_section = True
                node.title_norm = VALUED_SECTIONS_INDEX[ beauty_name ]

            else:
                node.title_norm = beauty_name

            # hierarhy
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

            # sections index
            parent.sections[ beauty_name ] = node

        else:
            # text block
            last.lexems.append( lexem )

    return root


def mark_explanations( toc: TocNode ):
    # find POS node
    # find 1st list in childs
    # set flags:
    #   is_explanation
    #   is_example
    for lang_node in toc.find_lang_section():
        for node in lang_node.find_part_of_speech_section():
            # part-of-speech found
            # find 1st li
            for c in node:
                if c.is_list:
                    # 1st list found
                    # set flags
                    c.is_explanation_root = True
                    c.title = 'Explanations'

                    li_node: TocNode
                    for li_node in c.find_all( recursive=True ):
                        li_node.is_explanation_node = True

                        if li_node.lexems[0].base.endswith('#'):
                            li_node.is_explanation = True
                        elif li_node.lexems[0].base.endswith(':'):
                            li_node.is_example = True

                    break # stop. and go to next POS


def extract_raw_text( toc ) -> list:
    #     extract sense raw-text
    #       nodes for convert raw to text
    #       explanation
    #       explanation-example
    #       {{trans-top|...}}
    #       =synonyms= /  Li
    #     fill node.sense_raw

    raws = []

    for node in toc.find_all( recursive=True ):
        if node.is_explanation:
            # explanation.raw-text
            li = node.lexems[0]
            raws.append( li.raw )
        elif node.is_example:
            # explanation example.raw-text
            li = node.lexems[0]
            raws.append( li.raw )
        else:
            # templates
            for lexem in node.find_lexem( recursive= True ):
                if isinstance( lexem, Template):
                    t = lexem
                    if t.name == 'sense':
                        raw = t.arg(0, raw=True)
                        raws.append( raw )

                    elif t.name == 'trans-top':
                        raw = t.arg(0, raw=True)
                        raws.append( raw )

                    elif t.name == 'trans-see':
                        raw = t.arg(0, raw=True)
                        raws.append( raw )

                    elif t.name == 'ws sense':
                        raw = t.arg(0, raw=True)
                        raws.append( raw )

                    elif t.name in {
                        'en-noun',
                        'en-verb,',
                        'en-adj',
                        'en-adv',
                        'en-prep',
                        'en-inter',
                        'en-symbol',
                        'en-punctuationmark',
                        'en-proverb',
                        'en-propn',
                        'en-propernoun',
                        'en-proper-noun',
                        'en-prop',
                        'en-pron',
                        'en-pronoun',
                        'en-prepphrase',
                        'en-phrase',
                        'en-prepositionalphrase',
                        'en-preposition',
                        'en-pp',
                        'en-prep',
                        'en-prefix',
                        'en-suffix',
                        'en-pluralnoun',
                        'en-plural-noun',
                        'en-pastof',
                        'en-particle',
                        'en-part',
                        'en-intj',
                        'en-interjection',
                        'en-inter',
                        'en-interj',
                        'en-initialism',
                        'en-ingformof',
                        'en-det',
                        'en-decades',
                        'en-contraction',
                        'en-cont',
                        'en-conjunction',
                        'en-conj',
                        'en-conj-simple',
                        'en-con',
                        'en-comparativeof',
                        'en-cat',
                        'en-adverb',
                        'en-adv',
                        'en-adj',
                        'en-abbr',
                    }:
                        raw = t.raw
                        raws.append( raw )

    return raws


def group_by_sense( toc: TocNode ) -> TocNode:
    for node in toc:
        for lexem in node.lexems:
            if isinstance( lexem, Template ):
                t = lexem
                if t.name == 'trans-top':
                    # do grouping

                    # 1. read rest. expect Template.name == 'trans-bottom'. skip Template.name == 'trans-mid'
                    # 2. take text or Li. pass to the make_tree(). get root. set title = 'trans-top'. add to the node. set flag trans_top = True

                    # node
                    #   - text
                    #   - {{trans-top|....\}}
                    #   - *
                    #   - *
                    #   - *
                    #   - {{trans-bottom}}
                    #   - text
                    #
                    # to
                    #
                    # node text
                    # node 'trans-top'
                    # node text

                    # root
                    #   node
                    #   node
                    #   node
                    #
                    # replace with
                    #
                    # root
                    #   trans_top_node
                    #     node
                    #     node
                    #     node

                    #                        sense
                    # explanation              x
                    # {{trans-top|...}} / li   x
                    # =synonyms= / li          x
                    # =sense= / li             x
                    # {{sense|...}}            x
                    pass

        group_by_sense( node )

    return toc


def extract_explanations(root: TocNode) -> tuple:
    explanations = []
    lexems2 = []

    # find first list block
    iterator = iter(root.lexems)

    # find first Li
    for lexem in iterator:
        if isinstance(lexem, Li):
            # found
            explanations.append(lexem)
            break
        else:
            lexems2.append(lexem)

    # find rest li
    for lexem in iterator:
        if isinstance(lexem, Li):
            explanations.append(lexem)   # examples here also
        else:
            break

    # save rest lexems
    for lexem in iterator:
        lexems2.append(lexem)

    return (explanations, lexems2)


def make_explanations_tree( lexems: list ) -> TocNode:
    # make toc
    # Add childs to parents
    # Add examples to explanations
    def is_a_contain_b( a: TocNode, b: TocNode ) -> bool:
        a_base = a.lexems[0].base
        b_base = b.lexems[0].base

        if b_base.startswith( a_base ):
            if b_base == a_base:
                return False
            else:
                return True
        else:
            return False

    root = TocNode()
    root.title = 'Explanations'
    root.is_explanation_root = True
    last = root

    for li in lexems:
        node = TocNode()
        node.title = li.raw
        node.is_explanation_node = True
        node.is_li = True
        node.lexems.append( li )

        if li.base.endswith('#'):
            node.is_explanation = True

        if li.base.endswith(':'):
            node.is_example = True

        if last is root:
            root.append( node )
            last = node

        elif is_a_contain_b( last, node ):
            last.append( node )
            last = node

        else:
            while last is not root:
                if is_a_contain_b( last, node ):
                    break
                else:
                    last = last.parent

            last.append( node )
            last = node

    return root


def make_li_tree( lexems: list ) -> TocNode:
    # make toc
    # Add childs to parents
    # Add examples to explanations
    def is_a_contain_b( a: TocNode, b: TocNode ) -> bool:
        pa_base = a.lexems[0].base
        li_base = b.lexems[0].base

        if li_base.startswith( pa_base ):
            if li_base == pa_base:
                return False
            else:
                return True
        else:
            return False

    root = TocNode()
    root.title = 'list'
    root.is_list_root = True
    last = root

    for li in lexems:
        node = TocNode()
        node.is_li = True
        node.title = li.raw
        node.lexems.append( li )

        if last is root:
            root.append( node )
            last = node

        elif is_a_contain_b( last, node ):
            last.append( node )
            last = node

        else:
            while last is not root:
                if is_a_contain_b( last, node ):
                    break
                else:
                    last = last.parent

            last.append( node )
            last = node

    return root


# def find_translations_in_sections_in_trans_see(node: TocNode) -> WikictionaryItem:
#     # {{trans-see|cat|cat/translations#Noun}}
#     from ..Scrapper_Wiktionary_WikitextParser import parse
#
#     item = WikictionaryItem()
#
#     for lexem in node.lexems:
#         if isinstance(lexem, Template):
#             t = lexem
#             if t.name == 'trans-see':
#                 gloss = t.arg(0)
#                 title = t.arg(1)
#                 if title:
#                     spits = title.split( '#', maxsplit=1 )
#                     page_title    = spits[0].strip()
#                     section_title = spits[1] if len(spits) > 1 else ''
#
#                     if page_title:
#                         # meke http request
#                         text = Scrapper_Wiktionary_RemoteAPI.get_wikitext( page_title )
#
#                         # parse
#                         lexems = parse(text)
#                         toc    = make_toc(lexems)
#
#                         # scrap translations
#                         for trnode in toc.find_all( recursive=True ):
#                             scrap_translations( trnode, with_trans_seee=False )
#
#                         # merge translations
#                         for trnode in toc.find_all( recursive=True ):
#                             item.TranslationsBySentence.update( trnode.item.TranslationsBySentence )
#                             item.TranslationsByLang.update( trnode.item.TranslationsByLang )
#
#     return item


# def scrap_translations(node: TocNode, with_trans_seee=True):
#     """
#     :param node:
#     :param with_trans_seee:  for prevent recursion
#     :return:
#     """
#     for sec in node:
#         if sec.title.lower().strip() in VALUED_SECTIONS[ ws.TRANSLATIONS ]:
#             translations  = find_translations_in_sections_in_trans_top( sec )
#             node.item.TranslationsBySentence = translations
#
#             if with_trans_seee:
#                 item = find_translations_in_sections_in_trans_see( sec )
#                 node.item.TranslationsBySentence.update( item.TranslationsBySentence )
#                 node.item.TranslationsByLang = item.TranslationsByLang


#
def get_label_type( expl, item ):
    from Scrapper_Helpers import convert_to_alnum, deduplicate, proper, get_lognest_word
    from ..Scrapper_Wiktionary_WikitextParser import Li, Dl, Link, String

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


def group_by_class( lexems: list ):
    # chains:
    # - lexem: Header
    # - lexem: Li
    # - lexem: Li
    # - lexem: Li
    # - lexem: String
    # to groups:
    # - (Header, (lexem))
    # - (Li    , (lexem, lexem, lexem))
    # - (str   , (lexem))

    class keyfn:
        def __init__(self):
            self.expect = None  # ( key, expect_class, expect_name )

        def __call__(self, x, *args, **kwargs):
            if self.expect:
                (key, expect_class, expect_name) = self.expect
                if isinstance( x, expect_class ) and x.name == expect_name:
                    self.expect = None
                    return key
                else:
                    return key

            else:
                if isinstance( x, Header ):
                    return Header
                # elif isinstance( x, Li ):
                #     return Li
                # elif isinstance( x, Dl ):
                #     return Dl
                # elif isinstance( x, Template ) and x.name == 'trans-top':
                #     self.expect = ( 'trans-top', Template, 'trans-bottom' )
                #     return 'trans-top'
                else:
                    return str

    yield from itertools.groupby( lexems, keyfn() )


def make_tree_from_groups( root: TocNode ) -> TocNode:
    # =====Synonyms=====
    # See also [[Thesaurus:cat]], [[Thesaurus:man]].
    # {{checksense|en}}
    # * {{sense|any member of the [[suborder]] (sometimes [[superfamily]]) [[Feliformia]] or [[Feloidea]]}} {{l|en|feliform}} ("[[cat-like]]" [[carnivoran]]), [[feloid]] (compare [[Caniformia]], {{taxlink|Canoidea|superfamily|noshow=1|ver=170212}})
    # * {{sense|any member of the [[subfamily]] [[Felinae]], genera ''[[Puma]]'', ''[[Acinonyx]]'', ''[[Lynx]]'', ''[[Leopardus]]'', and ''[[Felis]]'')}} {{l|en|feline cat}}, a [[feline]]
    # * {{sense|any member of the subfamily [[Pantherinae]], genera ''[[Panthera]], [[Uncia]]'' and ''[[Neofelis]]''}} {{l|en|pantherine cat}}, a [[pantherine]]
    #
    # to
    # node: root
    #   node: Synonyms
    #     node: tx
    #       - See also [[Thesaurus:cat]], [[Thesaurus:man]].
    #       - {{checksense|en}}
    #    node: li
    #      node: li
    #        - * {{sense|any member of the [[suborder]] (sometimes [[superfamily]]) [[Feliformia]] or [[Feloidea]]}} {{l|en|feliform}} ("[[cat-like]]" [[carnivoran]]), [[feloid]] (compare [[Caniformia]], {{taxlink|Canoidea|superfamily|noshow=1|ver=170212}})
    #      node: li
    #        - * {{sense|any member of the [[subfamily]] [[Felinae]], genera ''[[Puma]]'', ''[[Acinonyx]]'', ''[[Lynx]]'', ''[[Leopardus]]'', and ''[[Felis]]'')}} {{l|en|feline cat}}, a [[feline]]
    #      node: li
    #        - * {{sense|any member of the subfamily [[Pantherinae]], genera ''[[Panthera]], [[Uncia]]'' and ''[[Neofelis]]''}} {{l|en|pantherine cat}}, a [[pantherine]]

    # last
    last = root

    # group lexems by class
    for k, group in group_by_class( root.lexems ):
        # make tree branches: li, dl, tx
        if k is Li:
            # Li block
            node = TocNode()
            node.title = 'li'
            node.is_li = True
            node = make_li_tree( node, group )
            last.append( node )
        else:
            # text block
            node = TocNode()
            node.title = 'tx'
            node.is_tx = True
            node.lexems = list( group )
            last.append( node )

    return root


def convert_lists_to_tree( root : TocNode ) -> TocNode:
    make_tree_from_groups( root )

    # recursive
    for node in root:
        convert_lists_to_tree( node )

    return root


def get_leaf_explanation_nodes( root: TocNode ) -> list:
    leaf_explanations = []

    for node in root:
        if node.is_leaf_explanation:
            leaf_explanations.append( node )

        # recursive
        leaf_explanations.extend( get_leaf_explanation_nodes( node ) )

    return leaf_explanations


def add_explanations( toc: TocNode ):
    for node in toc.find_part_of_speech_section():
        (explanations, lexems2) = extract_explanations( node )

        node.lexems = lexems2

        extree = make_explanations_tree( explanations )
        node.explanations = extree

        node.append( extree )


def make_lists_same_length( a: list, b: list ):
    if len( a ) == len( b ):
        return
    elif len( a ) > len( b ):
        b.extend( itertools.repeat( '', len(a) - len(b) ) )
    elif len( a ) < len( b ):
        a.extend( itertools.repeat( '', len(b) - len(a) ) )


# def convert_items_raw_to_txt( page_title: str, items: list ) -> list:
#     raws = [ ]
#
#     for item in items:
#         raws.append( item.ExplainationRaw )
#         raws.append( item.ExplainationExamplesRaw )
#
#     converted = Scrapper_Wiktionary_RemoteAPI.expand_templates( page_title, raws )
#     itreaator = iter( converted )
#
#     for item in items:
#         item.ExplainationTxt = next( itreaator )
#         item.ExplainationExamplesTxt = next( itreaator )
#
#         # beautify
#         item.ExplainationTxt = item.ExplainationTxt.lstrip( '#*: ' )
#         item.ExplainationExamplesTxt = item.ExplainationExamplesTxt.lstrip( '#*: ' )
#
#     return items


def convert_raw_to_txt( page_title: str, raws: list ) -> list:
    converted = Scrapper_Wiktionary_RemoteAPI.expand_templates( page_title, raws )
    return converted


# def attach_translations( items: list ) -> list:
#     # attach translations
#     # group items by IndexPartOfSpeech
#     groups = [ (k, list( g )) for k, g in itertools.groupby( items, key=lambda item: item.IndexPartOfSpeech) ]
#
#     # get lists
#     for k, group in groups:
#         # make package
#         explanations = []
#         tr_sentences = []
#
#         for item in group:
#             explanations.append( item.ExplainationTxt )
#             tr_sentences.extend( item.TranslationsBySentence.keys() )
#
#         # unique
#         tr_sentences = list( set( tr_sentences ) )
#
#         # if has translations only
#         if tr_sentences:
#             # make same length
#             #make_lists_same_length( explanations, tr_sentences )
#
#             # request to api
#             pairs = Scrapper_IxiooAPI.Match_List_PKS_With_Lists_Of_PKS( explanations, tr_sentences )
#
#             # attach
#             for item, (e, t) in zip(group, pairs):
#                 item.TranslationSentence = t
#                 item.TranslationsPairs   = pairs
#                 try:
#                     by_lang = item.TranslationsBySentence[ t ]
#                     item.Translation_EN.extend( by_lang.get( EN, [] ) )
#                     item.Translation_FR.extend( by_lang.get( FR, [] ) )
#                     item.Translation_DE.extend( by_lang.get( DE, [] ) )
#                     item.Translation_ES.extend( by_lang.get( ES, [] ) )
#                     item.Translation_IT.extend( by_lang.get( IT, [] ) )
#                     item.Translation_PT.extend( by_lang.get( PT, [] ) )
#                     item.Translation_RU.extend( by_lang.get( RU, [] ) )
#
#                 except KeyError:
#                     pass
#
#     return items


def get_synonyms_by_sentences( node: TocNode ) -> list:
    syns = []

    # find 'Synonyms' section
    for node in node:
        if node.title == 'Synonyms':
            # found
            # find list elements: li
            for lexem in node.lexems:
                if isinstance( lexem, Li ):
                    # found
                    # fetch all synonyms
                    pass

    return syns


def attach_synonyms( pos_node: TocNode ) -> list:
    # attach synonyms

    # get node explanations
    #   fetch explanations
    # get node synonyms (from subsection)
    #   fetch synonyms list (by sentence)
    #   fetch from: https://en.wiktionary.org/wiki/Thesaurus:cat

    # =====Synonyms=====
    # * {{sense|any member of the [[suborder]] (sometimes [[superfamily]]) [[Feliformia]] or [[Feloidea]]}} {{l|en|feliform}} ("[[cat-like]]" [[carnivoran]]), [[feloid]] (compare [[Caniformia]], {{taxlink|Canoidea|superfamily|noshow=1|ver=170212}})
    # * {{sense|any member of the [[subfamily]] [[Felinae]], genera ''[[Puma]]'', ''[[Acinonyx]]'', ''[[Lynx]]'', ''[[Leopardus]]'', and ''[[Felis]]'')}} {{l|en|feline cat}}, a [[feline]]
    # * {{sense|any member of the subfamily [[Pantherinae]], genera ''[[Panthera]], [[Uncia]]'' and ''[[Neofelis]]''}} {{l|en|pantherine cat}}, a [[pantherine]]

    syns = get_synonyms_by_sentences( pos_node )

    return pos_node


def mark_leaf_explanation_nodes( root: TocNode ):
    has_childs_with_explanation = False

    # recursive
    for child in root:
        has_in_childs = mark_leaf_explanation_nodes( child )
        if has_in_childs:
            has_childs_with_explanation = True

    # check
    if root.is_explanation:
        if has_childs_with_explanation is False:
            root.is_leaf_explanation = True
        return True
    else:
        return has_childs_with_explanation


def update_index_in_toc( root, level=0, prefix="", index_pos=''  ):
    # text counter
    # list counter
    # header counter
    # li counter
    i = 0
    counter = collections.Counter()
    counter['text'] = 0
    counter['list'] = 0
    counter['li'] = 0
    counter['*'] = 0
    counter[':'] = 0
    # counter['trans_top'] = 0

    node: TocNode
    for node in root:
        if node.is_header:
            i += 1
            node.index_in_toc = prefix + str( i ) + '.'

        elif node.is_explanation_root:
            node.index_in_toc = prefix + 'ex.'

        elif node.is_text:
            # skip i. add 'text' + text_index
            counter[ 'text' ] += 1
            node.index_in_toc = prefix + '"' + str( counter[ 'text' ] ) + '.'

        elif node.is_list:
            #
            counter[ 'list' ] += 1
            node.index_in_toc = prefix + '[' + str( counter['list'] ) + '].'

        elif node.is_example:
            #
            counter[ ':' ] += 1
            node.index_in_toc = prefix + ':' + str( counter[':'] ) + '.'

        elif node.is_li and not node.is_explanation:
            #
            counter[ '*' ] += 1
            node.index_in_toc = prefix + '*' + str( counter['*'] ) + '.'

        elif node.is_li:
            #
            counter[ 'li' ] += 1
            node.index_in_toc = prefix + str( counter['li'] ) + '.'

        elif node.is_trans_top:
            #
            counter[ 'trans_top' ] += 1
            node.index_in_toc = prefix + '.trans_top-' + str( counter['trans_top'] ) + '.'
        else:
            #print ( node, node.is_li )
            pass

        # index_in_pos
        if node.is_pos:
            node.index_pos = node.index_in_toc
        else:
            node.index_pos = index_pos

        # recursive
        update_index_in_toc( node, level+1, node.index_in_toc, node.index_pos )


def remove_other_langs( toc: TocNode ):
    to_remove = []
    to_keep = []

    # find current lang
    # get root node
    # remove all other sections
    for node in toc.find_all( recursive=True ):
        if node.is_lang and node.title_norm in LANG_SECTIONS_INDEX:
            to_keep.append( node )

    # collect nodes tor remove
    if to_keep:
        for lang in to_keep:
            for node in lang.parent:
                if node is lang:
                    pass
                else:
                    to_remove.append( node )

            # remove
            for node in to_remove:
                lang.parent.remove( node )


def trans_see_finder( toc ):
    for node in toc.find_all( recursive=True ):
        for t in node.find_lexem( recursive=True ):
            if isinstance( t, Template):
                if t.name == 'trans-see':
                    print(node.title, (node, t), t.raw)
                    yield (node, t)

def add_translations_from_trans_see( page, toc: TocNode ):
    # 1. find all {{trans-see|...}}
    # 2. request page via wiktionary API
    # 3. parse page -> lexemes + toc
    # 4. make search index:  dict[ English ][ Noun ][ Translations ] = node
    # 5. check: dict[ English ][ Noun ] == current_node.part_of_speech
    # 6. get trarnslations. add to node =Translations=

    # 1. find all {{trans-see|...}}
    node: TocNode
    for node, t in trans_see_finder( toc ):
        # found
        full_url = t.arg( 1 )

        if full_url is None:
            continue

        # split cat/translations#Noun  ->  (cat/translations, Noun)
        page_url = full_url.split('#')[0]

        # skip self
        if page_url == page.label:
            continue

        # 2. request to wiktionary API
        raw_text = Scrapper_Wiktionary_RemoteAPI.get_wikitext( page_url )

        # 3. parse page -> lexemes + toc
        ts_lexemes = Scrapper_Wiktionary_WikitextParser.parse( raw_text )
        ts_toc = make_tree( ts_lexemes )
        ts_toc.dump()

        # 4. make search index:  dict[ English ][ Noun ][ Translations ] = (node, t)
        # example:
        #    English
        #      Noun
        #        Translations
        #          {{trans-top}}
        #      Verb
        d = {}
        # find =Translations=
        for nd in ts_toc.find_all( recursive=True ):
            if nd.title_norm in VALUED_SECTIONS[ ws.TRANSLATIONS ]:
                ts = nd
                pos = ts.get_parent_pos_node()
                lang = pos.get_parent_lang_node()
                # dict[ English ][ Noun ][ Translations ] = node
                d \
                    .setdefault( lang.title_norm, {} ) \
                    .setdefault( pos.title_norm, {} ) \
                    .setdefault( ts.title_norm, nd )

        # 5. check:
        #    dict[ English ][ Noun ][ Translations ]
        #    dict[ English ][ Translations ]
        #    dict[ Translations ]
        #    dict[ English ][ Noun ]
        #    dict[ Noun ]
        #    dict[ English ]
        #    {{trans-top}}
        current_ts = node
        current_pos = current_ts.get_parent_pos_node()
        current_lang = current_pos.get_parent_lang_node()
        try:
            ts_translations_node = d[ current_lang.title_norm ][ current_pos.title_norm ][ current_ts.title_norm ]
        except KeyError:
            ts_translations_node = None

        # 6. get all from =Trarnslations=. add to node =Translations=
        if ts_translations_node is not None:
            # append lexemes
            node.lexems.extend( ts_translations_node.lexems )


def scrap( page: Scrapper_Wiktionary.Page ) -> List[WikictionaryItem]:
    # 1. get Page: id, ns, title, raw-text
    # 2. parse raw-text -> take lexemes
    # 3. keep lexemes. make table-of-contents (toc). toc structure is tree. each branch is header. each node hold lexemes
    # 4. take tree. find part-of-speech nodes. take lexemes. find li. convert li to nodes. it is explanations
    # 5. take each node. take lexemes. convert lists to tree, wrap text text block with node.
    items  = []

    lexems = page.to_lexems()
    page.lexems = lexems

    # make table-of-contents (toc)
    toc = make_tree( lexems )
    page.toc = toc
    remove_other_langs( toc )

    # add explanations
    add_explanations( toc )
    mark_leaf_explanation_nodes( toc )
    explanaions = get_leaf_explanation_nodes( toc )
    page.explanations = explanaions

    # add translations from {{trans-see|...}}
    add_translations_from_trans_see( page, toc )

    # add toc-numbers
    update_index_in_toc( toc )
    #toc.dump( with_lexems=False )

    # '{{...}}' -> 'Text'
    # 1. collect all valued raw-text:
    #      explanation-raw
    #      {{sense|...}}
    #      {{trans-top|...}}
    # 2. convert
    #    send raw to Wiktionary API
    #    get txt
    # 3. save
    #    saved = {}
    #    saved[ raw ] = txt
    #    page.raw_txt = saved

    # 1. collect
    raws = extract_raw_text( toc )

    # 2. convert raw to txt
    txts = convert_raw_to_txt( page.label, raws )

    # clean li
    txts_cleaned = []
    for raw, txt in zip( raws, txts ):
        if raw.startswith( '#' ) or raw.startswith( '*' ) or raw.startswith( ':' ):
            txts_cleaned.append( txt.lstrip( '#*: ' ) )
        else:
            txts_cleaned.append( txt )
    txts = txts_cleaned

    # 3. save
    page.text_by_raw = dict( zip( raws, txts ) )

    # update explanation raw, txt
    for node in page.explanations:
        node.sense_raw = node.lexems[ 0 ].raw
        node.sense_txt = page.text_by_raw[ node.sense_raw ]

    # Prepare for scrap
    # now, get all explanation senses
    explanation_by_sense = { }

    for e in page.explanations:
        explanation_by_sense[ e.sense_txt ] = e

    page.explanation_by_sense = explanation_by_sense

    # get lang module with definitions
    import importlib
    lm = importlib.import_module("wiktionary.en.Scrapper_Wiktionary_" + 'EN' + '_Definitions')

    # Scrap
    # each explanation
    for i, node in enumerate( page.explanations, start=1 ):
        item = node.item

        # base attributes
        item.LabelName = page.label
        item.LanguageCode = 'en'
        item.SelfUrl = "https://en.wiktionary.org/wiki/" + page.label
        item.Sense = node.sense_txt

        # Index
        item.IndexinPage = i
        item.IndexinToc = node.index_in_toc
        item.IndexPartOfSpeech = node.index_pos

        # Synonyms, Antonyms, Troponyms, Holonyms, Translations_*,...
        check_node( page, node, lm )

        # type
        pos_node = node.get_parent_pos_node()
        item.Type = PART_OF_SPEECH_SECTIONS_INDEX[ pos_node .title.lower().strip() ]

        # explanation text
        item.ExplainationRaw = node.sense_raw
        item.ExplainationTxt = node.sense_txt

        # Example
        for example_node in node.find_examples():
            item.ExplainationExamplesRaw = example_node.lexems[0].raw
            item.ExplainationExamplesTxt =  page.text_by_raw[ item.ExplainationExamplesRaw ]
            break  # first only

        # LabelType
        item.LabelType = get_label_type( node.lexems[0], item )

        # PrimaryKey
        label_type = item.LabelType if item.LabelType else ""
        item.PrimaryKey = item.LanguageCode + "-" + item.LabelName + "§" + label_type + "-" + str( item.IndexinPage )

        items.append( item )

    return  items


# Explanation
# #
#
# Translations
# *
# *
# *
#
# Synonyms
# *
# *
# *
#

# extract sentences
# TocNode
#   Li - sense
#   Li - sense
#   Li - sense

# 1 Explanation - 1 Sentence
# node
#   raw, human_text

# node.id  ->  <span id="node-id">...raw...</span>  ->  id, human_text  ->  node.id,
#                                                                           node.raw,
#                                                                           node.human
#                                                                           node.sense
#                                                                           node.words

# section, id,




# 1. from Explanation:
#    from templates                              -> Syn
# 2. in section Synonyms
#    - if exists list
#        - group by list
#          - with sense
#          - without sense
#      else
#        - from Templates
#          - with sense
#          - without sense
#
#    if exist {{sense}} - group by sense
#      then collect to packet
#      then request to API
#      then attach to explanation
# 3. Etymology
#    add to each explanation                    -> syn
# 4. Verb
#    add to each explanation                    -> syn
# 5. Interjection
#    add to each explanation                    -> syn
# 6. Adjective, Dl, Dt                          -> syn
# 7. Alternative forms                          -> synonym of alternate form?
#
# .. where {{syn}} exists ?
#


# matcher
# explanations
#   # explanation
#   # explanation
#   # explanation
# ==section===
# * (sentence) [[word]]
# * (sentence) [[word]]
# * (sentence) [[word]]
#
# match_pks( explanations_block, section_block )
# match_pks( explanations_node, synonyms_node )
# match_pks( explanations_node, hyponyms_node )
# match_pks( explanations_node, translations_node )

# Lang
#  POS
#   Explanations
#   Synonyms
#
# Lang
#  Etymology
#   POS
#    Explanations
#    Synonyms
#
# Lang
#  Etymology
#   POS
#    Explanations
#   Synonyms
#
# if Explanations == 1
#   take all synonyms
# if Explanations > 1
#   take synonyms by sentence: explanation.txt -> synonym.sense.txt

# TOC
# Node
#   explanations = []   # leafs. ex: explanations = [ node, node, node ]
#   sections = {}       # ex: sections[ synonyms ] = [ items ]

# Page
#   toc
#     lang
#       etymology
#         noun              # POS
#           explanations    # explanations
#           synonyms
#         synonyms
#       synonyms
#
#   toc-node
#     explanations          #
#     parent                # -> lang
#     childs                # []
#     sections              # [lang].    [synonyms, antonyms]

# matcher
#   match
#     explanation.txt
#     section / list / item.sense


# 1. raw-text
# 2. lexemes
# 3. Table-Of-Contents (toc)
#    toc-node structure:
#      node
#        title
#        sections
#        explanations
# 3a. load external pages:
#    lang
#      'translations'
#        section[ 'translations' ]
#          trans-see|...
#      'synonyms'
#        section[ 'synonyms' ]
#          Thesaurus:...
# 4. get leaf explanations only
#    explanations[]
# 5. scrap
#      for each leaf_explanation:
#        attach:
#          explanations > 1:
#            5.1. attach section
#                find section 'synonyms' in order: explanation / pos / etymology / lang
#                  get senses, cache
#                 .by_senses = extract_senses()
#                  if sections[ 'synonyms' ] has senses:
#                    get by_senses
#                    get matches pks
#                    for each explanation:
#                      attach_section( 'synonyms', pks_matched_sentence )
#                  if sections[ 'synonyms' ] without senses:
#                    attach_section( 'synonyms' )
#            5.2. attach child examples
#            5.3. attach parent explanations
#                   5.3.1 attach parent explanations child examples
#            5.4. attach parent sections: pos / etymology / lang
#          explanations == 1:
#                find section 'synonyms' in: explanation / pos / etymology / lang
#                  if sections[ 'synonyms' ] has senses:
#                    attach_section( 'synonyms' )
#                  if sections[ 'synonyms' ] without senses:
#                    attach_section( 'synonyms' )

# node
#   by_sense        # .by_sense[ 'sense text' ] = [ lexem, lexem, ]
#   no_sense        # .no_sense = [ lexem, lexem ]
#
# extract senses in section:
#   synonyms      : * {{sense|...}}
#   translations: : {{trans-top|...}
#
#   if thesaurus:
#     ={{ws sense|...}}=
#       =synonyms=
#         {{ws|word}}
#
# synonyms      : Thesaurus:... ->  =English= / =Noun= / ={{ws sense|...}}= / =Synonyms= / {{ws|...}}
# translations  : {{trans-see|...} -> =English= / =Noun= / =Translations= / {{trans-top|...}

# find synonyms
# in_section
#   toc / lang / etymology / pos
#     sections          # <- check title for 'synonyms'. sections is {}


# translations[ sense ] = Container
# synonyms[ sense ] = Container
# hyponyms[ sense ] = Container

# translations[ * ] = Container

# parse_translations():
#   return translations, sense, container

