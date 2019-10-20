import itertools
import collections
from collections import defaultdict
from typing import List
from Scrapper_Helpers import convert_to_alnum, deduplicate, proper, get_lognest_word
from wiktionary import Scrapper_Wiktionary
from wiktionary import Scrapper_Wiktionary_RemoteAPI
from wiktionary import Scrapper_Wiktionary_WikitextParser
from wiktionary.Scrapper_Wiktionary_Item import WikictionaryItem
from wiktionary.Scrapper_Wiktionary_Checkers import check_node
from wiktionary.Scrapper_Wiktionary_WikitextParser import Header, Template, Li, Dl, Link, String
from wiktionary.en.Scrapper_Wiktionary_EN_Sections import LANG_SECTIONS_INDEX, PART_OF_SPEECH_SECTIONS_INDEX, VALUED_SECTIONS_INDEX, VALUED_SECTIONS
from wiktionary.en.Scrapper_Wiktionary_EN_TableOfContents import \
    Section, Root, Lang, PartOfSpeech, ExplanationsRoot, section_map, Explanation, ExplanationExample, Translations, \
    ExplanationLi


def make_table_of_contents( lexemes: list ) -> Root:
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
                node.lexemes.append( header )

            elif beauty_name in PART_OF_SPEECH_SECTIONS_INDEX:
                # Part of speech
                node = PartOfSpeech()
                node.title = header.name
                node.title_norm = PART_OF_SPEECH_SECTIONS_INDEX[ beauty_name ]
                node.level = header.level
                node.lexemes.append( header )

            elif beauty_name in VALUED_SECTIONS_INDEX:
                # Synonyms, Antonyms, Translations
                cls = section_map.get( beauty_name, Section )
                node = cls()
                node.title = header.name
                node.title_norm = VALUED_SECTIONS_INDEX[ beauty_name ]
                node.level = header.level
                node.lexemes.append( header )

            else:
                # Any other section
                node = Section()
                node.title = header.name
                node.title_norm = beauty_name
                node.level = header.level
                node.lexemes.append( header )

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

        else:
            # text block
            last.lexemes.append( lexem )
            # index by class
            last.lexemes_by_class[ type( lexem ) ][ lexem.name ].append( lexem )

    return root


def extract_raw_text( toc: Root ) -> list:
    #     extract sense raw-text
    #       nodes for convert raw to text
    #       explanation
    #       explanation-example
    #       {{trans-top|...}}
    #       =synonyms= /  Li
    #     fill node.sense_raw

    raws = []

    for node in toc.find_all( Section, recursive=True ):
        if isinstance( node, Explanation ):
            # explanation.raw-text
            li = node.lexemes[0]
            raws.append( li.raw )
        elif isinstance( node, ExplanationExample ):
            # explanation example.raw-text
            li = node.lexemes[0]
            raws.append( li.raw )
        else:
            # templates
            for t in node.find_lexem( recursive=True ):
                if isinstance( t, Template ):
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


def make_explanations_tree( lexemes: list ) -> ExplanationsRoot:
    # make toc
    # Add childs to parents
    # Add examples to explanations
    def is_a_contain_b( a: Section, b: Section ) -> bool:
        a_base = a.lexemes[0].base
        b_base = b.lexemes[0].base

        if b_base.startswith( a_base ):
            if b_base == a_base:
                return False
            else:
                return True
        else:
            return False

    root = ExplanationsRoot()
    root.title = 'Explanations'
    last = root

    for li in lexemes:
        if li.base.endswith('#'):
            node = Explanation()
            node.title = li.raw
            node.lexemes.append( li )

        elif li.base.endswith(':'):
            node = ExplanationExample()
            node.title = li.raw
            node.lexemes.append( li )

        elif li.base.endswith('*'):
            node = ExplanationLi()
            node.title = li.raw
            node.lexemes.append( li )

        else:
            node = Explanation()
            node.title = li.raw
            node.lexemes.append( li )

        #
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


def get_label_type( expl, item ):
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


def get_leaf_explanation_nodes( root: Section ) -> list:
    leaf_explanations = []

    for node in root.find_explanation_sections():
        if node.is_leaf_explanation:
            leaf_explanations.append( node )

    return leaf_explanations


def add_explanations( toc: Root ):
    for node in toc.find_part_of_speech_sections():
        (explanations, lexems2) = node.extract_explanations()

        node.lexems = lexems2

        ex_tree = make_explanations_tree( explanations )

        node.append( ex_tree )


def make_lists_same_length( a: list, b: list ):
    if len( a ) == len( b ):
        return
    elif len( a ) > len( b ):
        b.extend( itertools.repeat( '', len(a) - len(b) ) )
    elif len( a ) < len( b ):
        a.extend( itertools.repeat( '', len(b) - len(a) ) )


def convert_raw_to_txt( page_title: str, raws: list ) -> list:
    converted = Scrapper_Wiktionary_RemoteAPI.expand_templates( page_title, raws )
    return converted


def mark_leaf_explanation_nodes( root: Root ):
    has_childs_with_explanation = False

    # recursive
    for child in root:
        has_in_childs = mark_leaf_explanation_nodes( child )
        if has_in_childs:
            has_childs_with_explanation = True

    # check
    if isinstance( root, Explanation ):
        if has_childs_with_explanation is False:
            root.is_leaf_explanation = True
        return True
    else:
        return has_childs_with_explanation


def update_index_in_toc( root: Section, level=0, prefix="", index_pos=''  ):
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

    node: Section
    for node in root:
        if isinstance( node, ExplanationsRoot ):
            node.index_in_toc = prefix + 'ex.'

        elif isinstance( node, ExplanationExample ):
            #
            counter[ ':' ] += 1
            node.index_in_toc = prefix + ':' + str( counter[':'] ) + '.'

        else:
            i += 1
            node.index_in_toc = prefix + str( i ) + '.'

        # index_in_pos
        if isinstance( node, PartOfSpeech ):
            node.index_pos = node.index_in_toc
        else:
            node.index_pos = index_pos

        # recursive
        update_index_in_toc( node, level+1, node.index_in_toc, node.index_pos )


def remove_other_langs( toc: Root ):
    to_remove = []
    to_keep = []

    # find current lang
    # get root node
    # remove all other sections
    for node in toc.find_all( Section, recursive=True ):
        if node.title_norm in LANG_SECTIONS_INDEX:
            to_keep.append( node )

    # collect nodes for remove
    if to_keep:
        for lang in to_keep:
            # take lang-same-level nodes
            for node in lang.parent:
                if node is lang:
                    pass
                else:
                    to_remove.append( node )

            # remove
            for node in to_remove:
                lang.parent.remove( node )


def trans_see_finder( toc: Root ):
    for node in toc.find_all( Translations, recursive=True ):
        for t in node.lexemes_by_class[ Template ][ 'trans-see' ]:
            yield (node, t)

def add_translations_from_trans_see( page, toc: Root ):
    # 1. find all {{trans-see|...}}
    # 2. request page via wiktionary API
    # 3. parse page -> lexemes + toc
    # 4. make search index:  dict[ English ][ Noun ][ Translations ] = node
    # 5. check:
    #      dict[ English ][ Noun ] == current_node.part_of_speech
    #      dict[ Noun ] == current_node.part_of_speech
    #      dict[ Translations ]
    # 6. get trarnslation lexemes. add to node =Translations=

    # 1. find all {{trans-see|...}}
    node: Translations
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

        # if page not exists - next
        if raw_text is None:
            continue

        # 3. parse page -> lexemes + toc
        ts_lexemes = Scrapper_Wiktionary_WikitextParser.parse( raw_text )
        ts_toc = make_table_of_contents( ts_lexemes )
        update_index_in_toc( ts_toc )
        # ts_toc.dump()

        # 4. make search index:  dict[ English ][ Noun ][ Translations ] = (node, t)
        # example:
        #    English
        #      Noun
        #        Translations
        #          {{trans-top}}
        #      Verb
        d = defaultdict( lambda: defaultdict( list ) )

        # find =Translations=
        for ts in ts_toc.find_all( Translations, recursive=True ):
            pos  = ts.get_parent_pos_node()   if ts  is not None   else None
            lang = pos.get_parent_lang_node() if pos is not None   else None

            spos  = pos.title_norm  if pos  is not None else None
            slang = lang.title_norm if lang is not None else None

            # dict[ English ][ Noun ] = translations_node
            d[ slang ][ spos ] = ts

            # English / Verb / Translations     ->      English / Verb / Translations   - is better better better
            # Verb / Translations               ->      None    / Verb / Translations   - is better better
            # English / Translations            ->      English / None / Translations   - is better
            # English / Synonyms / Translations ->      None    / None / Translations   - is good
            # Translations                      ->      None    / None / Translations   - is good


        # 5. check:
        #    dict[ English ][ Verb ][ Translations ]
        #    dict[ English ][ None ][ Translations ]
        #    dict[ None    ][ Verb ][ Translations ]
        #    dict[ None    ][ None ][ Translations ]
        #    {{trans-top}}
        current_ts   = node
        current_pos  = current_ts.get_parent_pos_node()
        current_lang = current_pos.get_parent_lang_node()   if current_pos is not None   else None

        cpos  =  current_pos.title_norm  if current_pos  is not None   else None
        clang =  current_lang.title_norm if current_lang is not None   else None

        #
        checks = [
            d[ clang ][ cpos ],     # ib betted betted betted
            d[ clang ][ None ],     # ib betted betted
            d[ None  ][ cpos ],     # ib betted
            d[ None  ][ None ],     # ib good
        ]

        # 6. get all from external page =Trarnslations=.
        #    add to node =Translations=
        ts_translations_node: Translations
        for ts_translations_node in filter( None, checks ):
            # append lexemes
            node.lexemes.extend( ts_translations_node.lexemes )
            # update index
            # index by class
            for lexem in ts_translations_node.lexemes:
                node.lexemes_by_class[ type( lexem ) ][ lexem.name ].append( lexem )


def update_popularity_of_word( item ):
    item.PopularityOfWord = 0

    if item.ExplainationExamplesRaw is not None:
        item.PopularityOfWord += len( item.ExplainationExamplesRaw ) * 5

    if item.RelatedTerms is not None:
        item.PopularityOfWord += len( item.RelatedTerms )

    other_cost = 0

    if item.Translation_DE is not None:
        other_cost += len( item.Translation_DE )

    if item.Translation_EN is not None:
        other_cost += len( item.Translation_EN )

    if item.Translation_ES is not None:
        other_cost += len( item.Translation_ES )

    if item.Translation_FR is not None:
        other_cost += len( item.Translation_FR )

    if item.Translation_IT is not None:
        other_cost += len( item.Translation_IT )

    if item.Translation_PT is not None:
        other_cost += len( item.Translation_PT )

    if item.Translation_RU is not None:
        other_cost += len( item.Translation_RU )

    if item.Holonymy is not None:
        other_cost += len( item.Holonymy )

    if item.Troponymy is not None:
        other_cost += len( item.Troponymy )

    if item.Hypernymy is not None:
        other_cost += len( item.Hypernymy )

    if item.Hyponymy is not None:
        other_cost += len( item.Hyponymy )

    if item.Meronymy is not None:
        other_cost += len( item.Meronymy )

    if item.Synonymy is not None:
        other_cost += len( item.Synonymy )

    if item.Antonymy is not None:
        other_cost += len( item.Antonymy )

    item.PopularityOfWord += 1 if other_cost else 0



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
    toc = make_table_of_contents( lexems )
    page.toc = toc
    remove_other_langs( toc )

    # add explanations
    add_explanations( toc )
    mark_leaf_explanation_nodes( toc )

    # get all lead explanations
    explanations = get_leaf_explanation_nodes( toc )
    page.explanations = explanations

    # add translations from {{trans-see|...}}
    add_translations_from_trans_see( page, toc )

    # add toc-numbers
    update_index_in_toc( toc )
    #toc.dump()

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
    raws = list( filter( None, raws ) )

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

    # 3. keep
    page.text_by_raw = dict( zip( raws, txts ) )

    # update explanation raw, txt
    for node in page.explanations:
        node.sense_raw = node.get_sense()

        # get raw of #
        # concatenate with parents
        sense = page.text_by_raw[ node.get_sense() ]
        parent = node.parent
        while parent is not None and isinstance( parent, (Explanation, ExplanationLi) ):
            sense = page.text_by_raw[ parent.get_sense() ] + ': ' + sense
            parent = parent.parent
        node.sense_txt = sense


    # Prepare for scrap
    # now, get all explanation senses
    explanation_by_sense = { }

    for e in page.explanations:
        explanation_by_sense[ e.sense_txt ] = e

    page.explanation_by_sense = explanation_by_sense

    # get lang module with definitions
    import importlib
    lm = importlib.import_module("wiktionary.en.Scrapper_Wiktionary_" + 'EN' + '_Definitions')

    indexinPage = 0

    # Scrap
    # each explanation
    for node in page.explanations:
        item = node.item

        # base attributes
        item.LabelName     = page.label
        item.LanguageCode  = 'en'
        item.SelfUrl       = "https://en.wiktionary.org/wiki/" + page.label
        item.TypeLabelName = node.get_parent_pos_node().title
        item.Senses['.']   = node.sense_txt

        # Index
        indexinPage += 1
        item.IndexinPage       = indexinPage
        item.IndexinToc        = node.index_in_toc
        item.IndexPartOfSpeech = node.index_pos

        # Synonyms, Antonyms, Troponyms, Holonyms, Translations_*,...
        check_node( page, node, lm )

        # type
        pos_node = node.get_parent_pos_node()
        item.Type = PART_OF_SPEECH_SECTIONS_INDEX[ pos_node .title.lower().strip() ]

        # explanation text
        item.ExplainationRaw = node.get_sense()
        item.ExplainationTxt = page.text_by_raw[ item.ExplainationRaw ]
        item.DescriptionTxt  = node.sense_txt

        # Example
        for example_node in node.find_example_sections():
            item.ExplainationExamplesRaw = example_node.lexemes[0].raw
            item.ExplainationExamplesTxt = page.text_by_raw[ item.ExplainationExamplesRaw ]
            break  # first only

        # LabelType
        item.LabelType = get_label_type( node.lexemes[0], item )

        # PrimaryKey
        label_type = item.LabelType if item.LabelType else ""
        item.PrimaryKey = item.LanguageCode + "-" + item.LabelName + "§" + label_type + "-" + str( item.IndexinPage )

        # PopularityOfWord 
        update_popularity_of_word( item )
        items.append( item )

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

# When "Simple page":
# --------------------------------------------------
# Section( English )
#   Section( Noun )
#     Section( Translations )
#       senses = {
#           "sense 1": ...,
#           "sense 2": ...,
#       }
#
# When {{trans-see|sense-trans-see|label}} expanded:
# --------------------------------------------------
# Section( English )
#   Section( Noun )
#     Section( Translations )
#       senses = {
#           "sense 1": ...,
#           "sense 2": ...,
#           "sense-trans-see": ...,  <--  from 'catfish'/English/Noun/Translations/"sense-trans-see"/...
#
#           "type of fish": ...,  <--  from 'catfish'/English/Noun/Translations/<all senses>/<all languages>
#              all translations, from deep pages also
#           "fish of the genus Silurus": ...,  <---  it sense from  deep page
#       }

