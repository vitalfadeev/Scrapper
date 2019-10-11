import itertools
import string
import re
from typing import List
from collections import defaultdict
import Scrapper_IxiooAPI
from wiktionary import Scrapper_Wiktionary
from wiktionary import Scrapper_Wiktionary_RemoteAPI
from wiktionary.Scrapper_Wiktionary_Item import WikictionaryItem
from wiktionary.Scrapper_Wiktionary_ValuableSections import VALUABLE_SECTIONS as ws
from wiktionary.Scrapper_Wiktionary_WikitextParser import Section, Header, Template, Li, Link, String, Container
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
        self.title          = title                    # title             str
        self.title_norm     = ""                       # title_normal      str
        self.level          = level                    # level             int
        self.parent         = parent                   # parent            TocNode
        self.lexems         = []                       # section lexems    Container
        self.item           = WikictionaryItem()       # store             WiktionaryItem
        self.is_lang        = False
        self.is_pos         = False
        self.is_explanation = False
        self.is_example     = False
        self.index_in_toc   = ''
        self.index_pos      = ''

    def append(self, node) -> None:
        node.parent = self
        super().append(node)

    def find_all(self, recursive=False):
        for c in self:
            yield c

            if recursive:
                yield from c.find_all(recursive)

    def find_lexem(self, recursive=True):
        for lexem in self.lexems:
            yield lexem

            if recursive:
                yield from lexem.find_all( recursive )

    def find_parents( self ) -> list:
        parent = self.parent
        while parent:
            yield parent
            parent = parent.parent


    def find_lang_section( self ) -> List[ "TocNode" ]:
        yield from filter( lambda node: node.is_lang, self.find_all( recursive=True ) )


    def find_part_of_speech_section( self ) -> List[ "TocNode" ]:
        yield from filter( lambda node: node.is_pos, self.find_all( recursive=True ) )


    def find_explanations( self ) -> List[ "TocNode" ]:
        yield from filter( lambda node: node.is_explanation, self.find_all( recursive=True ) )


    def find_examples( self ) -> List[ "TocNode" ]:
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


    def update_index_in_toc(self, level=0, prefix="", i=1, index_pos=None):
        # skip root
        if level == 0:
            for i, child in enumerate(self, start=1):
                child.update_index_in_toc(level+1, prefix, i, index_pos)

        else:
            # update
            num = prefix + str(i) + '.'
            self.index_in_toc = num
            if self.is_pos:
                index_pos = num
            self.index_pos = index_pos

            # recursive
            for i, child in enumerate(self, start=1):
                child.update_index_in_toc(level+1, num, i, index_pos)

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


    def __repr__(self):
        if self.is_lang:
            return self.title
        elif self.is_pos:
            return self.title
        elif self.is_explanation:
            return self.title
        elif self.is_example:
            return self.title
        else:
            return self.title


def make_toc(lexems: list) -> TocNode:
    """ Make table of contents """
    root = TocNode()
    last = root

    # 1. scan each lexem
    # 2. get Headers
    # 3. make tree
    for lexem in lexems:
        if isinstance(lexem, Header):
            header = lexem

            node = TocNode( title=header.name, level=header.level )
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
                node.title_norm = VALUED_SECTIONS_INDEX[ beauty_name ]

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

        else:
            # add sections elements
            last.lexems.append( lexem )

    return root


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


def make_explanations_tree(lexems: list) -> TocNode:
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
    last = root

    for li in lexems:
        node = TocNode()
        node.title = li.raw
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


def convert_raw_to_txt( page_title: str, items: list ) -> list:
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


def scrap(page: Scrapper_Wiktionary.Page) -> List[WikictionaryItem]:
    items  = []

    lexems = page.to_lexems()
    #lexems = replace_templates( lexems )
    toc    = make_toc( lexems )
    toc    = add_explanations( toc )
    toc    = toc.update_index_in_toc()
    #toc.dump( with_lexems=False )

    indexInPage = 0

    # scrap
    import importlib
    lm = importlib.import_module("wiktionary.en.Scrapper_Wiktionary_" + 'EN' + '_Definitions')

    for node in toc.find_all(recursive=True):
        #if node.index_in_toc == '1.2.1.':
            check_node( node, lm )
            scrap_translations( node )

    # merge
    # lang
    for lang_node in toc.find_lang_section():
        # part of speech
        for part_of_speech_node in lang_node.find_part_of_speech_section():
            pos_item = part_of_speech_node.merge_with_parents()

            # explanations
            for explanations_node in part_of_speech_node.find_explanations():
                explain = explanations_node.lexems[0]

                # we have lang, type, explain
                # print( lang_section.header.name, part_of_speech_section.header.name, explain )

                item = explanations_node.merge_with_childs()
                item.merge( pos_item )

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


    items = convert_raw_to_txt( page.label, items )
    items = attach_translations( items )

    # clean, unique
    for item in items:
        item.Synonymy = \
            filter( bool,
                    filter( lambda s: s != item.LabelName,
                            map( filterWodsProblems, item.Synonymy ) ) )
        item.Synonymy = unique( item.Synonymy )

    return items


