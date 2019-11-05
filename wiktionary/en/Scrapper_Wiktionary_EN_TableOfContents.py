from typing import Iterator
from collections import defaultdict
from wiktionary.Scrapper_Wiktionary_ValuableSections import VALUABLE_SECTIONS as ws
from Scrapper_WikitextParser import Template, Li, Container
from wiktionary.Scrapper_Wiktionary_Item import WiktionaryItem

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
        self.thesaurus = []
        # indexes
        self.sections_by_name = {}
        self.lexemes_by_class = defaultdict( lambda: defaultdict( list ) )
        self.lexemes_by_sense = defaultdict( list )


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


    def find_lang_sections( self ) -> Iterator[ "Lang" ]:
        yield from self.find_all( Lang, recursive=True )


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
        return {}


    def dump( self, level=0, show_me=None ):
        # print header
        if level == 0:
            # recursive
            for i, child in enumerate( self, start=1 ):
                child.dump( level+1, show_me )
            return

        # print node
        # short. title only
        if show_me is not None and self is show_me:
            print( "  " * level + repr(self) + '  <---  i here' )
        else:
            print( "  " * level + repr(self) )

        # recursive
        for child in self:
            child.dump( level+1, show_me )


    def __repr__(self):
        return self.index_in_toc + ' ' + self.title


class Root(Section):
    pass


class Lang(Section):
    pass


class PartOfSpeech(Section):
    pass


class ExplanationsRoot( Section ):
    pass


class Explanation(Section):
    def __init__(self):
        super().__init__()
        self.item = WiktionaryItem()
        self.is_leaf_explanation = False
        self.sense_raw = None
        self.sense_txt = None

    def get_sense( self ):
        # get raw of #
        # concatenate with parents
        return self.lexemes[0].raw


class ExplanationExample(Section):
    pass


class ExplanationLi(Section):
    pass


class Translations( Section ):
    def get_lexemes_by_sense( self ):
        # find {{tans-top}}
        return dict( trans_top_reader( self.lexemes ) )


class AnyYms(Section):
    def get_lexemes_by_sense( self ):
        # find * {{sense}}
        return dict( li_sense_reader( self.lexemes ) )

class Synonyms(AnyYms): pass
class Antonyms(AnyYms): pass
class Hyponyms(AnyYms): pass
class Hypernyms(AnyYms): pass
class Troponyms(AnyYms): pass
class Holonyms(AnyYms): pass
class Meronyms(AnyYms): pass


section_map = {
    ws.TRANSLATIONS: Translations,
    ws.SYNONYMS: Synonyms,
    ws.ANTONYMS: Antonyms,
    ws.HYPONYMS: Hyponyms,
    ws.HYPERNYMS: Hypernyms,
    ws.TROPONYMS: Troponyms,
    ws.HOLONYMS: Holonyms,
    ws.MERONYMS: Meronyms,
}
