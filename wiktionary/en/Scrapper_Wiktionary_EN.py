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
from wiktionary.Scrapper_Wiktionary_WikitextParser import Section, Header, Template, Li, Dl, Link, String, Container
from wiktionary.en.Scrapper_Wiktionary_EN_Sections import LANG_SECTIONS_INDEX, PART_OF_SPEECH_SECTIONS_INDEX, VALUED_SECTIONS_INDEX, VALUED_SECTIONS
from wiktionary.en import Scrapper_Wiktionary_EN_Templates
from ..Scrapper_Wiktionary_Checkers import check_node
from Scrapper_Helpers import unique, filterWodsProblems

EN = 'en'
DE = 'de'
PT = 'pt'
FR = 'fr'
IT = 'it'
ES = 'es'
RU = 'ru'


class TocNode(list):
    def __init__(self, title='', level=0, parent=None):
        super().__init__()
        self.title               = title                    # title             str
        self.title_norm          = ""                       # title_normal      str
        self.level               = level                    # level             int
        self.parent              = parent                   # parent            TocNode
        self.lexems              = []                       # section lexems    Container
        self.item                = WikictionaryItem()       # store             WiktionaryItem
        self.is_lang             = False
        self.is_pos              = False
        self.is_valued_section   = False
        self.is_explanation      = False
        self.is_example          = False
        self.index_in_toc        = ''
        self.index_pos           = ''
        self.is_li               = False
        self.is_list             = False
        self.is_text             = False
        self.is_header           = False
        self.is_trans_top        = False
        self.is_explanation_root = False
        self.is_explanation_node = False
        self.sense_raw           = ""
        self.sense_txt           = ""
        self.is_leaf_explanation = False

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


    def update_index_in_toc(self, level=0, prefix=""):
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
        for node in self:
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
                print ( node, node.is_li )

            # recursive
            node.update_index_in_toc(level+1, node.index_in_toc)

        return self


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
    for k, group in group_by_class( lexems ):
        if k is Header:
            for header in group:
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

        elif k is Li:
            # list block
            node = make_li_tree( group )
            node.is_list = True
            last.append( node )

        elif k == 'trans-top':
            # Translations in trans_top. Grouped by sense
            node = TocNode()
            node.title = "trans-top"
            node.is_trans_top = True
            node.lexems = list( group )
            last.append( node )

        else:
            # text block
            node = TocNode()
            node.title = "text"
            node.is_text = True
            node.lexems = list( group )
            last.append( node )

    return root


def mark_explanations( toc: TocNode ) -> TocNode:
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

    return toc


def extract_sense_raw_text( toc ) -> dict:
    #     extract sense raw-text
    #       nodes for convert raw to text
    #       explanation
    #       explanation-example
    #       {{trans-top|...}}
    #       =synonyms= /  Li
    #     fill node.sense_raw

    senses = {}  # example: senses["1.2.1.1."] = "An animal of the family Felidae"

    for node in toc.find_all( recursive=True ):
        if node.is_explanation:
            li = node.lexems[0]
            node.sense_raw = li.raw
        elif node.is_example:
            li = node.lexems[0]
            node.sense_raw = li.raw
        elif node.is_trans_top:
            t = node.lexems[ 0 ]
            node.sense_raw = t.arg(0)
        elif node.title_norm == ws.SYNONYMS or node.title_norm == ws.HYPONYMS:
            for li_node in node.find_all( recursive=True ):
                if li_node.is_li:
                    li = li_node.lexems[0]
                    # check {{sense|...}}
                    # if ok
                    #   get from {{sense|...}}
                    # else
                    #   get all li
                    for tt in li.find_objects( Template, recursive=False ):
                        # {{sense|...}} detected
                        if tt.name in ['sense', 's'] :
                            li_node.sense_raw = next( tt.args() ).raw
                            break
                    else:
                        # {{sense|...}} not found
                        # get all raw-text
                        li_node.sense_raw = li.raw

        if node.sense_raw:
            senses[node.index_in_toc] = node.sense_raw

    return senses


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
    root.title = 'Explanations'
    root.is_explanation_root = True
    last = root

    for li in lexems:
        node = TocNode()
        node.title = li.raw
        node.is_explanation_node = True
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


def find_translations_in_sections_in_trans_top(node: TocNode) -> dict:
    """
    :param node:
    :return:  dict   translations[ sentence ][ lang ] = ['term1', 'term2', term3']
    """
    # {{trans-top|domestic species}}
    # ...
    # German: {{q|♂♀}} {{t+|de|Katze|f}}, {{q|♂}} {{t+|de|Kater|m}}, {{q|♀}} {{t+|de|Kätzin|f}}, {{t|de|Pantoffeltiger|m}} {{q|humorous}}
    # ...
    # {{trans-bottom}}
    translation_templates = {'t', 't+'}
    lexems = node.lexems
    iterator = iter(lexems)
    translations = defaultdict(lambda: defaultdict(list))  # translations[ sentence ][ lang ] = ['term1', 'term2', term3']

    # find start. Start is Template {{trans-top|...}}
    for e in iterator:
        if isinstance(e, Template) and e.name == 'trans-top':
            # start found
            template = e
            sentence = template.arg(0)

            # find end. End is Template {{trans-bottom}}
            for e in iterator:
                if isinstance(e, Template) and e.name == 'trans-bottom':
                    # end found
                    break

                elif isinstance(e, Li): # translations in format: * English {{t|...}}
                    # get translations
                    # *Abkhaz: {{t | ab | ацгә}}
                    # *Acehnese: {{t | ace | mië}}
                    # *Adyghe: {{t | ady | кӏэтыу}}
                    #print(e.raw)
                    try:
                        language = e.childs[0].raw.strip(': \n').lower()
                        lang = Scrapper_Wiktionary_EN_Templates.TRANSLATION_LANGS[language ]

                        texts = []
                        for c in e.childs[1:]:
                            if isinstance(c, Template):
                                t = c
                                if t.name in translation_templates:
                                    texts.extend( Scrapper_Wiktionary_EN_Templates.to_words( t ) )

                        translations[sentence][lang].extend( texts )

                    except AttributeError:
                        pass
                    except KeyError:
                        pass
                    except IndexError:
                        pass

    # dump translations
    # for sent, by_lang in translations.items():
    #     print(sent)
    #     for lang, terms in by_lang.items():
    #         print( "  ", lang, " ".join(terms) )

    return translations


def find_translations_in_sections_in_trans_see(node: TocNode) -> WikictionaryItem:
    # {{trans-see|cat|cat/translations#Noun}}
    from ..Scrapper_Wiktionary_WikitextParser import parse

    item = WikictionaryItem()

    for lexem in node.lexems:
        if isinstance(lexem, Template):
            t = lexem
            if t.name == 'trans-see':
                gloss = t.arg(0)
                title = t.arg(1)
                if title:
                    spits = title.split( '#', maxsplit=1 )
                    page_title    = spits[0].strip()
                    section_title = spits[1] if len(spits) > 1 else ''

                    if page_title:
                        # meke http request
                        text = Scrapper_Wiktionary_RemoteAPI.get_wikitext( page_title )

                        # parse
                        lexems = parse(text)
                        toc    = make_toc(lexems)

                        # scrap translations
                        for trnode in toc.find_all( recursive=True ):
                            scrap_translations( trnode, with_trans_seee=False )

                        # merge translations
                        for trnode in toc.find_all( recursive=True ):
                            item.TranslationsBySentence.update( trnode.item.TranslationsBySentence )
                            item.TranslationsByLang.update( trnode.item.TranslationsByLang )

    return item


def scrap_translations(node: TocNode, with_trans_seee=True):
    """
    :param node:
    :param with_trans_seee:  for prevent recursion
    :return:
    """
    for sec in node:
        if sec.title.lower().strip() in VALUED_SECTIONS[ ws.TRANSLATIONS ]:
            translations  = find_translations_in_sections_in_trans_top( sec )
            node.item.TranslationsBySentence = translations

            if with_trans_seee:
                item = find_translations_in_sections_in_trans_see( sec )
                node.item.TranslationsBySentence.update( item.TranslationsBySentence )
                node.item.TranslationsByLang = item.TranslationsByLang


#
def get_label_type(expl, item):
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
                elif isinstance( x, Li ):
                    return Li
                elif isinstance( x, Dl ):
                    return Dl
                elif isinstance( x, Template ) and x.name == 'trans-top':
                    self.expect = ( 'trans-top', Template, 'trans-bottom' )
                    return 'trans-top'
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


def add_explanations(toc: TocNode) -> TocNode:
    for node in toc.find_part_of_speech_section():

        (explanations, lexems2) = extract_explanations( node )

        node.lexems = lexems2

        extoc = make_explanations_tree( explanations )

        node.append( extoc )

    return toc



def make_lists_same_length( a: list, b: list ):
    if len( a ) == len( b ):
        return
    elif len( a ) > len( b ):
        b.extend( itertools.repeat( '', len(a) - len(b) ) )
    elif len( a ) < len( b ):
        a.extend( itertools.repeat( '', len(b) - len(a) ) )


def convert_items_raw_to_txt( page_title: str, items: list ) -> list:
    raws = [ ]

    for item in items:
        raws.append( item.ExplainationRaw )
        raws.append( item.ExplainationExamplesRaw )

    converted = Scrapper_Wiktionary_RemoteAPI.expand_templates( page_title, raws )
    itreaator = iter( converted )

    for item in items:
        item.ExplainationTxt = next( itreaator )
        item.ExplainationExamplesTxt = next( itreaator )

        # beautify
        item.ExplainationTxt = item.ExplainationTxt.lstrip( '#*: ' )
        item.ExplainationExamplesTxt = item.ExplainationExamplesTxt.lstrip( '#*: ' )

    return items


def convert_raw_to_txt( page_title: str, raws: dict ) -> dict:
    converted = Scrapper_Wiktionary_RemoteAPI.expand_templates( page_title, raws )
    return converted


def attach_translations( items: list ) -> list:
    # attach translations
    # group items by IndexPartOfSpeech
    groups = [ (k, list( g )) for k, g in itertools.groupby( items, key=lambda item: item.IndexPartOfSpeech) ]

    # get lists
    for k, group in groups:
        # make package
        explanations = []
        tr_sentences = []

        for item in group:
            explanations.append( item.ExplainationTxt )
            tr_sentences.extend( item.TranslationsBySentence.keys() )

        # unique
        tr_sentences = list( set( tr_sentences ) )

        # if has translations only
        if tr_sentences:
            # make same length
            #make_lists_same_length( explanations, tr_sentences )

            # request to api
            pairs = Scrapper_IxiooAPI.Match_List_PKS_With_Lists_Of_PKS( explanations, tr_sentences )

            # attach
            for item, (e, t) in zip(group, pairs):
                item.TranslationSentence = t
                item.TranslationsPairs   = pairs
                try:
                    by_lang = item.TranslationsBySentence[ t ]
                    item.Translation_EN.extend( by_lang.get( EN, [] ) )
                    item.Translation_FR.extend( by_lang.get( FR, [] ) )
                    item.Translation_DE.extend( by_lang.get( DE, [] ) )
                    item.Translation_ES.extend( by_lang.get( ES, [] ) )
                    item.Translation_IT.extend( by_lang.get( IT, [] ) )
                    item.Translation_PT.extend( by_lang.get( PT, [] ) )
                    item.Translation_RU.extend( by_lang.get( RU, [] ) )

                except KeyError:
                    pass

    return items


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


def scrap(page: Scrapper_Wiktionary.Page) -> List[WikictionaryItem]:
    # 1. get Page: id, ns, title, raw-text
    # 2. parse raw-text -> take lexemes
    # 3. keep lexemes. make table-of-contents (toc). toc structure is tree. each branch is header. each node hold lexemes
    # 4. take tree. find part-of-speech nodes. take lexemes. find li. convert li to nodes. it is explanations
    # 5. take each node. take lexemes. convert lists to tree, wrap text text block with node.

    items  = []

    lexems = page.to_lexems()
    toc    = make_tree( lexems )
    toc    = mark_explanations( toc )
    toc    = toc.update_index_in_toc()
    _      = mark_leaf_explanation_nodes( toc )
    #toc.dump( with_lexems=False )

    # dump explanations:
    # for node in toc.find_all( recursive=True ):
    #     if node.is_leaf_explanation:
    #         print( node.index_in_toc, node.sense_txt )

    # preparing for attaching translations to explanations, synonyms to explanations
    #   preparing for conversion via Wiktionary API:
    #     extract sense raw-text
    #       nodes for convert raw to text
    #       explanation
    #       explanation-example
    #       {{trans-top|...}}
    #       =synonyms= /  Li
    #     fill node.sense_raw
    #   convert
    #     fill node.sense_txt
    senses = extract_sense_raw_text( toc )
    # toc.dump_sense_raw()

    # convert raw to txt
    converted = convert_raw_to_txt( page.label, senses )

    # save txt values
    for node in toc.find_all( recursive=True ):
        if node.sense_raw:
            # update sense
            node.sense_txt = converted[ node.index_in_toc ].lstrip("#*: ")
            # update explanation-txt
            if node.is_explanation:
                node.item.ExplainationTxt = converted[ node.index_in_toc ].lstrip("#*: ")
            # update explanation-example-txt
            if node.is_example:
                node.item.ExplainationExamplesTxt = converted[ node.index_in_toc ].lstrip("#*: ")


    #toc.dump_sense_txt()

    # attach
    #   translations -> explanations
    #   synonyms -> explanations

    indexInPage = 0

    # get lang module with definitions
    import importlib
    lm = importlib.import_module("wiktionary.en.Scrapper_Wiktionary_" + 'EN' + '_Definitions')

    # scrap
    # each node
    for lang_node in toc.find_lang_section():
        for node in lang_node.find_all( recursive=True ):
            # if node.index_in_toc == '1.2.1.1.[1].5.':
                check_node( node, lm )
                #scrap_translations( node )

                node.item.PrimaryKey = node.index_in_toc
                node.item.Sense = node.sense_txt
                items.append( node.item )


    # merge
    # 0. find leaf explanation-nodes
    #    example:
    #      # A person:                                   <- [FAIL] not leaf
    #        ## (offensive) A spiteful or angry woman.   <- [ OK ]  is leaf
    #        ## An enthusiast or player of jazz          <- [ OK ]  is leaf
    #
    # 1. trans-top
    #      if match sense -> explanation txt
    #        merge
    #
    # 2. example
    #    example -> parent explanations
    #
    # 3. synonyms
    #      if match sense -> explanation txt
    #        merge

    # 1. trans-top
    trans_top_nodes = {}
    explanation_nodes = {}

    # prepare
    # take translation senses. for matching
    for lang_node in toc.find_lang_section():
        for node in lang_node.find_all( recursive=True ):
            # in trans-top
            if node.is_trans_top:
                if node.sense_txt:
                    trans_top_nodes[ node.sense_txt ] =  node

    # take explanation senses. for matching
    for lang_node in toc.find_lang_section():
        for node in lang_node.find_all( recursive=True ):
            # in explanation
            if node.is_leaf_explanation:
                if node.sense_txt:
                    explanation_nodes[ node.sense_txt ] =  node
                    # dump explanations:
                    # print( node.index_in_toc, node.sense_txt )

    # find mattch.
    # request to match API
    pairs = Scrapper_IxiooAPI.Match_List_PKS_With_Lists_Of_PKS(
        list( explanation_nodes.keys() ),
        list( trans_top_nodes.keys() )
    )

    # attach
    for e_sense, t_sense in pairs:
        # if not null
        if e_sense and t_sense:
            # get node
            e_node = explanation_nodes[ e_sense ]
            t_node = trans_top_nodes[ t_sense ]
            # merge
            e_node.item.merge( t_node.item )
            # save translation sense
            e_node.item.SenseFromTranslations = t_sense

    # 2. leaf node
    #     - merge with all parents ( before this each parent was merged with valued childs )
    #     - merge with all child examples
    for lang_node in toc.find_lang_section():
        for node in lang_node.find_all( recursive=True ):
            if node.is_leaf_explanation:
                # merge with all parents
                pass

                # merge with child examples
                for c in node.find_all( recursive=True ):
                    if c.is_example:
                        node.item.merge( c.item )

    # 3. synonyms
    #    find section 'synonyms' under part-of-speech section.
    #      get senses
    #      call matcher API
    #      if match sense -> explanation txt
    #        merge
    for lang_node in toc.find_lang_section():
        for pos_node in lang_node.find_part_of_speech_section():
            for synonyms_node in pos_node.find_all( recursive=True ):
                # find section 'synonyms'
                if synonyms_node.title_norm == ws.SYNONYMS:
                    syn_sense_nodes = {}

                    # take all li nodes under section =synonyms=
                    for node in synonyms_node.find_all( recursive=True ):
                        if node.is_li:
                            if node.sense_txt:
                                # get sense
                                syn_sense_nodes[ node.sense_txt ] = node

                    # call matcher API
                    pairs = Scrapper_IxiooAPI.Match_List_PKS_With_Lists_Of_PKS(
                        list( explanation_nodes.keys() ),
                        list( syn_sense_nodes.keys() )
                    )

                    # dump syn matched pairs
                    # for ex, sy in pairs:
                    #     print("e:", ex)
                    #     print("s:", sy)
                    #pprint.pprint( pairs, width=80, depth=2 )

                    # attach
                    for e_sense, s_sense in pairs:
                        # if not null
                        if e_sense and s_sense:
                            # get node
                            e_node = explanation_nodes[ e_sense ]
                            s_node = syn_sense_nodes[ s_sense ]
                            # merge
                            e_node.item.merge( s_node.item )
                            # save synonym sense
                            e_node.item.SenseFromSynonyms = s_sense

    # take explanations only
    # items2 = []
    # for lang_node in toc.find_lang_section():
    #     for pos_node in lang_node.find_part_of_speech_section():
    #         for explanation_node in pos_node.find_explanations():
    #             if explanation_node.is_leaf_explanation:
    #                 items2.append( explanation_node.item )

    items = []

    # lang
    for lang_node in toc.find_lang_section():
        # part of speech
        for part_of_speech_node in lang_node.find_part_of_speech_section():
            pos_item = part_of_speech_node.merge_with_parents()

            # explanations
            for explanations_node in part_of_speech_node.find_explanations():
                if explanations_node.is_leaf_explanation:
                    explain = explanations_node.lexems[0]

                    # we have lang, type, explain
                    # print( lang_section.header.name, part_of_speech_section.header.name, explain )

                    #item = explanations_node.merge_with_childs()
                    #item.merge( pos_item )
                    item = explanations_node.item

                    # base attributes
                    item.LabelName         = page.label
                    item.LanguageCode      = 'en'
                    item.SelfUrl           = "https://en.wiktionary.org/wiki/" + page.label

                    # Index
                    indexInPage += 1
                    item.IndexinPage       = indexInPage
                    item.IndexinToc        = explanations_node.index_in_toc
                    item.IndexPartOfSpeech = explanations_node.index_pos

                    # type
                    item.Type              = PART_OF_SPEECH_SECTIONS_INDEX[part_of_speech_node.title.lower().strip()]

                    # Explanation
                    item.ExplainationRaw   = explain.raw
                    item.ExplainationTxt   = explain.get_text()

                    # Example
                    for example_node in explanations_node.find_examples():
                        item.ExplainationExamplesRaw = example_node.lexems[0].raw
                        break  # first only

                    # LabelType
                    item.LabelType         = get_label_type( explain, item )

                    # PrimaryKey
                    label_type             = item.LabelType if item.LabelType else ""
                    item.PrimaryKey        = item.LanguageCode + "-" + item.LabelName + "§" + label_type + "-" + str(item.IndexinPage)

                    items.append(item)


    return items


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

