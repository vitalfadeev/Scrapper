from typing import Iterator
from functools import lru_cache
from collections import defaultdict
import Scrapper_IxiooAPI
from wiktionary.Scrapper_Wiktionary_ValuableSections import VALUABLE_SECTIONS as ws
from wiktionary.Scrapper_Wiktionary_WikitextParser import Header, Template, Li, Dl, Link, String, Container
from wiktionary.Scrapper_Wiktionary_Item import WikictionaryItem

# High-level
# Root
#   Lang
#     Section               # Etymology / ...
#       PartOfSpeech        # Noun / Verb / ...
#           Explanation     #
#           Translations    #
#           Synonyms        #
#           Hyponyms        #

def trans_top_reader( lexemes: list ) -> Iterator[ tuple ]:
    """
    Read block from {{trans-top}} to {{trans-bottom}}
    Return reader.  Reader return tuple (sense, lexemes)
    :param lexems:
    :return:  Iterator[ ( str, list) ]  # example: ('cat fish', [...]), ('domestic species', [...]),
    """
    reader = iter( lexemes )

    # find block
    for t in reader:
        if isinstance( t, Template ) and t.name == 'trans-top':
            # save sense
            sense = t.arg( 0, raw=True )

            # skip block header
            next( reader, None )

            # block lexemes store
            grouped = []

            # read block
            for e in reader:
                if isinstance( e, Template ) and e.name == 'trans-bottom':
                    break
                else:
                    grouped.append( e )

            # return tuple
            yield (sense, grouped)


def li_sense_reader( lexemes: list ) -> Iterator[ tuple ]:
    reader = iter( lexemes )

    for li in reader:
        if isinstance( li, Li ):
            # find sense
            for s in li.childs:
                if s.name == 'sense':
                    sense = s.arg( 0, raw=True )
                    grouped = li.childs
                    yield ( sense, grouped )


# High-level
class Section(list):
    def __init__( self ):
        super().__init__()
        self.lexemes = []
        self.by_sense = {}
        self.title = ''
        self.title_norm = ''
        self.level = 0
        self.parent = None
        self.index_in_toc = ""
        # indexes
        self.sections_by_name = {}
        self.lexemes_by_class = defaultdict(lambda: defaultdict( list ))


    def append(self, node) -> None:
        node.parent = self
        super().append(node)


    def find_lexem(self, recursive=True) -> Iterator[ Container ]:
        # return node lexem and node lexem childs
        for lexem in self.lexemes:
            yield lexem

            if recursive:
                yield from lexem.find_all( recursive )


    def find_all(self, cls, recursive=False) -> Iterator["Section"]:
        for c in self:
            if isinstance(c, cls):
                yield c

            if recursive:
                yield from c.find_all(cls, recursive )


    def find_part_of_speech_sections( self ) -> Iterator[ "PartOfSpeech" ]:
        yield from self.find_all( PartOfSpeech, recursive=True )


    def find_explanation_sections( self ) -> Iterator["Explanation"]:
        yield from self.find_all( Explanation, recursive=True )


    def find_example_sections( self ) -> Iterator[ "ExplanationExample" ]:
        yield from self.find_all( ExplanationExample, recursive=True )


    def get_parent_pos_node( self ) -> "PartOfSpeech":
        node = self.parent

        while node is not None:
            if isinstance( node, PartOfSpeech ):
                return node
            else:
                node = node.parent

        return None


    def get_parent_lang_node( self ) -> "Lang":
        node = self.parent

        while node is not None:
            if isinstance( node, Lang ):
                return node
            else:
                node = node.parent

        return None


    def extract_explanations( self ) -> tuple:
        explanations = [ ]
        lexems2 = [ ]

        # find first list block
        iterator = iter( self.lexemes )

        # find first Li
        for lexem in iterator:
            if isinstance( lexem, Li ):
                # found
                explanations.append( lexem )
                break
            else:
                lexems2.append( lexem )

        # find rest li
        for lexem in iterator:
            if isinstance( lexem, Li ):
                explanations.append( lexem )  # examples here also
            else:
                break

        # save rest lexems
        for lexem in iterator:
            lexems2.append( lexem )

        return (explanations, lexems2)


    def get_lexemes_by_sense( self ):
        ...


    def dump( self, level=0 ):
        # print header
        if level == 0:
            # recursive
            for i, child in enumerate( self, start=1 ):
                child.dump( level+1 )
            return

        # print node
        # short. title only
        print("  " * level + self.index_in_toc + ' ' + repr(self))

        # recursive
        for child in self:
            child.dump( level+1 )


    def __repr__(self):
        return self.title


class Root(Section):
    ...


class Lang(Section):
    ...


class PartOfSpeech(Section):
    ...


class Explanations(Section):
    ...


class Explanation(Section):
    def __init__(self):
        super().__init__()
        self.item = WikictionaryItem()
        self.is_leaf_explanation = False


class ExplanationExample(Section):
    ...


class ExplanationLi(Section):
    ...


class Translations( Section ):
    @lru_cache( maxsize=32 )
    def get_lexemes_by_sense( self ):
        # find {{tans-top}}
        return dict( trans_top_reader( self.lexemes ) )


class Synonyms(Section):
    @lru_cache( maxsize=32 )
    def get_lexemes_by_sense( self ):
        # find * {{sense}}
        return dict( li_sense_reader( self.lexemes ) )

    # def scrap_by_sense( self, sense ):
    #     pass
    #
    # def scrap_all( self ):
    #     pass
    #
    # def scrap( self, page, explanation ):
    #     if self.by_sense:
    #         self.scrap_by_sense( explanation.sense_txt )
    #     else:
    #         self.scrap_all()


section_map = {
    ws.TRANSLATIONS: Translations,
    ws.SYNONYMS: Synonyms,
}




class PksMatcher:
    @classmethod
    @lru_cache( maxsize=32 )
    def match( self, explanations: Explanations, section: Section ):
        e_sentences = list( explanations.by_sense.keys() )
        s_sentences = list( section.by_sense.keys() )

        if e_sentences and s_sentences:
            matches = Scrapper_IxiooAPI.Match_List_PKS_With_Lists_Of_PKS( e_sentences, s_sentences )
            return matches
        else:
            return None
