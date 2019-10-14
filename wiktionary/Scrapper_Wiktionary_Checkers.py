import more_itertools
from wiktionary.Scrapper_Wiktionary_WikitextParser import Section, Header, Template, Li, Link, String, Container


def valid( context, definition ):
    return any( check( context, definition ))


def check( context, definition ):
    for func, args in definition.items():
        yield from func( context, args )


def in_section( context, definitions: dict ):
    # check current section name or find parent section
    is_section_found = False
    next_checkers = None
    node = context

    while node is not None:
        if node.title_norm:
            if node.title_norm in definitions:
                is_section_found = True
                next_checkers = definitions[ node.title_norm ]
                break  # one time check context only
        node = node.parent

    if is_section_found:
        yield from check( context, next_checkers )


def in_trans_top( context, definitions ):
    # get translations
    # {{trans-top|...}}
    # *Abkhaz: {{t | ab | ацгә}}
    # *Acehnese: {{t | ace | mië}}
    # *Adyghe: {{t | ady | кӏэтыу}}

    node = context
    expect_langs = definitions.keys()

    if node.is_trans_top:
        for li in node.lexems:
            if isinstance( li, Li ):
                # try:
                    language_raw = li.childs[0].raw
                    language = language_raw.strip( ': \n' ).lower()

                    if language in expect_langs:
                        # if in arg [[...]]
                        #   take ...
                        # else
                        #   take arg text

                        result = list( check( li, definitions[ language ] ) )
                        yield from result

                        #yield from check( li, definitions[ language ] )

                # except AttributeError:
                #     pass
                # except KeyError:
                #     pass
                # except IndexError:
                #     pass

"""
def in_example( context, defs):
    for node in context:
        if node.is_example:
            yield from check( node, defs )
"""

def DICT( d ):
    result = {}
    for key, value in d.items():
        if isinstance(key, tuple):
            for k in key:
                result[k] = value
        else:
            result[ key ] = value

    return result



def if_explanation( context, defs ):
    if hasattr( context, 'is_explanation' ) and context.is_explanation:
        yield from check( context, defs )


def text_contain( context, definitions ):
    for text in definitions:
        if repr(context).find( text ) != -1:
            yield True


def in_template( context, definitions: dict ):
    for t in context.find_lexem( recursive=True ):
        if isinstance(t, Template):
            if t.name in definitions:
                yield from check( t, definitions[ t.name ] )


def in_template_trans_top( context, defs=None ):
    for t in context.find_lexem( recursive=True ):
        if isinstance(t, Template):
            if t.name == 'trans-top':
                pass


def with_lang( t, definitions ):
    lang = t.arg(0)
    if lang is None:
        lang = t.arg( 'lang' )

    if lang is None:
        yield from check( t, next( iter( definitions.values() ) ) )
    elif lang in definitions:
        yield from check( t, definitions[ lang ] )


def in_arg( context, definitions ):
    t = context
    arg_keys = definitions

    if isinstance(arg_keys, set):
        for k in arg_keys:
            yield from t.arg_links_or_text( k )

    elif isinstance( arg_keys, dict ):
        for k, definitions in arg_keys.items():
            a = t.arg( k )
            yield from check( a, definitions )

    else:
        raise Exception("unsupported")


def in_arg_by_lang( t, arg_keys ):
    lang = t.arg(0)
    if lang is None:
        lang = t.arg( 'lang' )

    if isinstance(arg_keys, set):
        for k in arg_keys:
            yield ( lang, t.arg( k ) )
    elif isinstance( arg_keys, dict ):
        for k, definitions in arg_keys.items():
            a = t.arg( k )
            for v in check( a, definitions ):
                yield ( lang, v )
    else:
        raise Exception("unsupported")


def in_any_arg( t, definitions ):
    for k, defs in definitions.items():
        for a in t.args():
            yield from check( a, defs )


def in_all_positional_args( t: Template, defs ):
    for a in t.positional_args():
        yield a.get_text()


def in_all_positional_args_except_lang( t: Template, defs ):
    args = list( t.positional_args() )
    for a in args[1:]:
        yield a.get_text()


def value_equal( a, expected ):
    if isinstance(expected, set):
        if a.get_text() in expected:
            yield True
    else:
        if a.get_text() == expected:
            yield True


def in_link( context, defs=None ):
    for lexem in context.find_lexem( recursive=True ):
        if isinstance( lexem, Link ):
            yield from lexem.to_words()


def has_template( context, tnames ):
    if isinstance( tnames, set ):
        for t in context.find_all( Template, recursive=True):
            if t.name in tnames:
                yield True
    else:
        raise Exception("unsupported")


def en_noun( context, defs ):
    yield from ()

def en_verb( context, defs ):
    yield from ()

def en_adj( context, defs ):
    yield from ()



def check_node( node, lm ):
    # 1. get from language module all vars. it is definitions
    # 2. in each definition take function and arguments. it is checker and arguments.
    # 3. recursive
    # 4 .run function with arguments. return words
    for name in filter( lambda s: s[0].isupper(), vars( node.item ) ):
        # if name == 'Synonymy':
        #     pass
        # else:
        #     continue

        if hasattr(lm, name):
            definitions = getattr( lm, name )
            definitions = detuple_dfinition_keys( definitions )
            generator = filter( None, check( node, definitions ) )

            store = getattr( node.item, name )

            if isinstance( store, list ):
                store.extend( generator )
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
        defs.update( to_append )

    return defs