from typing import Iterator
import more_itertools
from Scrapper_Helpers import filterWodsProblems, dict_merge
from wiktionary.Scrapper_Wiktionary_Matcher import Matcher
from wiktionary.Scrapper_Wiktionary_WikitextParser import Header, Template, Li, Link, String, Container
from wiktionary.en.Scrapper_Wiktionary_EN_TableOfContents import Explanation, ExplanationExample



def valid( page, explanation, context, definition ):
    return any( check( page, explanation, context, definition ))


def check( page, explanation, context, definition ):
    for func, args in definition.items():
        yield from func( page, explanation, context, args )


def in_all_parents( page, explanation, context, definitions ):
    explanation = context
    node = explanation.parent

    while node is not None:
        yield from check( page, explanation, node, definitions )

        node = node.parent


def in_section( page, explanation, context, definitions ):
    node = context

    # check each title
    # definitions[ 'synonyms' ] = {}
    for title, defs in definitions.items():
        section = node.sections_by_name.get( title, None )

        if section is not None:
            # do next check
            yield from check( page, explanation, section, defs )


def text_contain( page, explanation, context, definitions ):
    explanation = context
    for text in definitions:
        if explanation.sense_txt.find( text ) != -1:
            yield True


def in_template( page, explanation, context, definitions: dict ):
    for t in context.find_lexem( recursive=True ):
        if isinstance(t, Template):
            defs = definitions.get( t.name, None )
            if defs is not None:
                yield from check( page, explanation, t, defs )


def in_language( page, explanation, context, definitions: dict ):
    container = context
    expect_langs = definitions.keys()

    for li in container.find_objects( Li, recursive=False ):
        #    for each li:
        #       get first word. it is language
        language_raw = li.childs[ 0 ].raw
        language = language_raw.strip( ': \n' ).lower()

        if language in expect_langs:
            yield from check( page, explanation, li, definitions[ language ] )


def in_template_trans_top( page, explanation, context, defs=None ):
    for t in context.find_lexem( recursive=True ):
        if isinstance(t, Template):
            if t.name == 'trans-top':
                pass


def with_lang( page, explanation, t, definitions ):
    lang = t.arg(0)
    if lang is None:
        lang = t.arg( 'lang' )

    if lang is None:
        yield from check( page, explanation, t, next( iter( definitions.values() ) ) )
    elif lang in definitions:
        yield from check( page, explanation, t, definitions[ lang ] )


def in_arg( page, explanation, context, definitions ):
    t = context
    arg_keys = definitions

    if isinstance(arg_keys, set):
        for k in arg_keys:
            yield from t.arg_links_or_text( k )

    elif isinstance( arg_keys, dict ):
        for k, definitions in arg_keys.items():
            a = t.arg( k )
            yield from check( page, explanation, a, definitions )

    else:
        raise Exception("unsupported")


def in_arg_by_lang( page, explanation, t, arg_keys ):
    lang = t.arg(0)
    if lang is None:
        lang = t.arg( 'lang' )

    if isinstance(arg_keys, set):
        for k in arg_keys:
            yield ( lang, t.arg( k ) )
    elif isinstance( arg_keys, dict ):
        for k, definitions in arg_keys.items():
            a = t.arg( k )
            for v in check( page, explanation, a, definitions ):
                yield ( lang, v )
    else:
        raise Exception("unsupported")


def in_any_arg( page, explanation, t, definitions ):
    for k, defs in definitions.items():
        for a in t.args():
            yield from check( page, explanation, a, defs )


def in_all_positional_args( page, explanation, t: Template, defs ):
    for a in t.positional_args():
        yield a.get_text()


def in_all_positional_args_except_lang( page, explanation, t: Template, defs ):
    args = list( t.positional_args() )
    for a in args[1:]:
        yield a.get_text()


def value_equal( page, explanation, a, expected ):
    if isinstance(expected, set):
        if a.get_text() in expected:
            yield True
    else:
        if a.get_text() == expected:
            yield True


def equal_label( page, explanation, value, definitions ):
    expected = page.label
    if value == expected:
        yield True


def in_link( page, explanation, context, defs=None ):
    for lexem in context.find_lexem( recursive=True ):
        if isinstance( lexem, Link ):
            yield from lexem.to_words()


def has_template( page, explanation, context, tnames ):
    if isinstance( tnames, set ):
        for t in context.find_all( Template, recursive=True):
            if t.name in tnames:
                yield True
    else:
        raise Exception("unsupported")


def in_self( page, explanation, context, definitions ):
    yield from check( page, explanation, context, definitions )


def in_parent_explanations( page, explanation, context, definitions ):
    parent = context.parent

    while parent is not None and parent.is_explanation:
        yield from check( page, explanation, parent, definitions )

        parent = parent.parent


def in_all_parent_sections( page, explanation, context, definitions ):
    parent = context

    while parent is not None:
        if not isinstance( parent, Explanation ):
            yield from check( page, explanation, parent, definitions )

        parent = parent.parent


def in_examples( page, explanation, context, definitions ):
    for child in context:
        if isinstance(child, ExplanationExample):
            yield from check( page, explanation, child, definitions )


def by_sense( page, explanation, context, definitions ) -> Iterator:
    # 1. if single explaanation:
    #    get all from section (do next checkers)
    #
    # 2. if many explanations:
    #    if section without senses
    #      get all from sensed block (do next checkers)
    #
    #    if section has senses
    #      get senses
    #      do match
    #      if matched
    #        get all from sensed block (do next checkers)
    #
    section = context

    # 1. if single explanation
    if len( page.explanations ) == 1:
        # get all from section (do next checkers)
        container = Container()
        container.childs = section.lexemes
        yield from check( page, explanation, container, definitions )

    # 2. if many explanations
    elif len( page.explanations ) > 1:
        # section senses
        lexemes_by_sense = section.get_lexemes_by_sense()

        # translate sections senses from raw to txt
        section_senses = list( map( lambda s: page.text_by_raw[ s ], filter( None, lexemes_by_sense.keys() ) ) )

        # if section without senses
        if len( section_senses ) == 0:
            # get all from sensed block (do next checkers)
            lexemes = list( lexemes_by_sense.values() )  # all
            container = Container()
            container.childs = lexemes
            yield from check( page, explanation, container, definitions )  # call next checkers

        # if section has senses
        elif len( section_senses ) > 0:
            # get explanation sense
            explanation_sense_txt = explanation.sense_txt
            # get all explanations (for match all-at-once in matcher)
            explanation_sense_txts = map( lambda x: x.sense_txt, page.explanations )

            # match
            matched_txt = Matcher.match( explanation_sense_txt, explanation_sense_txts, section_senses )

            # save sense (for debugging)
            explanation.item.Senses[ type(section).__name__ ] = matched_txt

            if matched_txt:
                matched_raw = None

                # txt to raw
                for r, t in page.text_by_raw.items():
                    if t == matched_txt:
                        matched_raw = r
                        break

                lexemes = lexemes_by_sense.get( matched_raw, None )

                if lexemes:
                    # get all from sensed block (do next checkers)
                    container = Container()
                    container.childs = lexemes
                    yield from check( page, explanation, container, definitions )  # call next checkers


def en_noun( t, label ):
    """
    {{en-noun}}
    {{en-noun|es}}
    {{en-noun|...}}
    {{en-noun|...|...}}

    out: (single, [plural], is_uncountable)
    """
    s = label
    p = [ ]
    is_uncountable = False

    # http://en.wiktionary.org/wiki/Template:en-noun
    head = t.arg( "head" )
    head = head if head else label
    p1 = t.arg( 0 )
    p2 = t.arg( 1 )

    if p1 == "-":
        # uncountable
        is_uncountable = True

        if p2 == "s":
            # ends by s
            yield (None, head + "s", is_uncountable)

        elif p2 == "es":
            # ends by es
            yield (None, head + "es", is_uncountable)

        elif p2 is not None:
            # word
            yield (None, p2, is_uncountable)

    elif p1 == "~":
        # uncountable and countable
        is_uncountable = True

        if p2 == "s":
            # ends by s
            yield (None, head + "s", is_uncountable)

        elif p2 == "es":
            # ends by es
            yield (None, head + "es", is_uncountable)

        elif p2 is not None:
            # word
            yield (None, p2, is_uncountable)

        else:
            yield (None, head + "s", is_uncountable)

    elif p1 == "s":
        yield (None, head + "s", is_uncountable)

    elif p1 == "es":
        # add es
        yield (None, head + "es", is_uncountable)

    elif p1 is not None:
        # use term
        yield (None, p1, is_uncountable)

    elif p1 is None and p2 is None:
        yield (head, head + "s", is_uncountable)


def plural_en_noun( page, explanation, context, definitions ):
    t = context
    label = page.label
    (s, p, is_uncountable) = next( en_noun( t, label ) )

    if definitions:
        yield from check( page, explanation, p, definitions )
    else:
        yield p


def single_en_noun( page, explanation, context, definitions ):
    t = context
    label = page.label

    res = next( en_noun( t, label ), None )

    if res:
        (s, p, is_uncountable) = res

    if definitions:
        yield from check( page, explanation, s, definitions )
    else:
        yield s


def en_verb( page, explanation, context, defs ):
    yield from ()

def en_adj( page, explanation, context, defs ):
    yield from ()



def check_node( page, node, lm ):
    # 1. get from language module all vars. it is definitions
    # 2. in each definition take function and arguments. it is checker and arguments.
    # 3. recursive
    # 4 .run function with arguments. return words
    for name in filter( lambda s: s[0].isupper(), vars( node.item ) ):
        # if name == 'Translation_IT':
        #     pass
        # else:
        #     continue

        # get checker() from lang module
        # for Synonymy checker name is Synonymy
        if hasattr(lm, name):
            # prepare checkers
            definitions = getattr( lm, name )
            definitions = detuple_dfinition_keys( definitions )

            # run checker
            explanation = node
            generator = filter( None, check( page, explanation, node, definitions ) )

            # save result to item attribute
            store = getattr( node.item, name )

            if isinstance( store, list ):
                filtered = filter( filterWodsProblems, generator )
                cleaned = map( str.strip, filtered )
                store.extend( cleaned )
            elif isinstance( store, dict ):
                store.update( generator )
            elif isinstance( store, bool ) or store is bool:
                if any( generator ):
                    setattr( node.item, name, True )
            elif isinstance( store, str ):
                value = more_itertools.first_true( generator )
                if value:
                    setattr( node.item, name, value )
            # elif isinstance( store, int ):
            #     if value:
            #         setattr( node.item, name, value )
            # elif isinstance( store, float ):
            #     if value:
            #         setattr( node.item, name, value )
            else:
                raise Exception( "unsupported: " + str( type( store ) ) )


def checkers_from( page, explanation, context, definitions ):
    iterator = iter( definitions )

    # first. from module
    mod = {}
    defs =  getattr( mod, next( iterator ) )

    # rest. from definitions
    for key in iterator:
        defs = defs[ key ]

    yield from check( page, explanation, context, defs )


def detuple_dfinition_keys( defs ):
    to_append = {}
    to_remove = []

    #
    for k, v in defs.items():
        if isinstance(k, tuple):
            to_remove.append( k )
            to_append.update( dict.fromkeys(k, v) )

        if isinstance( v, dict ):
            detuple_dfinition_keys( v )

    # remove tupled keys
    for r in to_remove:
        defs.pop( r )

    # add un-tupled keys
    if to_append:
        dict_merge( defs, to_append )

    return defs
