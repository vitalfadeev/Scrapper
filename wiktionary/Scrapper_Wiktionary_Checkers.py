import more_itertools
from wiktionary.Scrapper_Wiktionary_WikitextParser import Section, Header, Template, Li, Link, String, Container


def valid( context, definition ):
    return any( check( context, definition ))


def check( context, definition ):
    for func, args in definition.items():
        yield from func( context, args )


def in_section( context, snames: dict ):
    for c in context:
        beauty_title = c.title.lower().strip()
        if beauty_title in snames:
            yield from check( c, snames[ beauty_title ] )


def in_section_pos( context, defs=None ):
    pass


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


def in_template( context, tnames: dict ):
    for t in context.find_lexem( recursive=True ):
        if isinstance(t, Template):
            if t.name in tnames:
                yield from check( t, tnames[ t.name ] )


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


def in_arg( t, arg_keys ):
    if isinstance(arg_keys, set):
        for k in arg_keys:
            yield t.arg( k )
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
    for name in filter( lambda s: s[0].isupper(), vars( node.item ) ):
        if hasattr(lm, name):
            definitions = getattr( lm, name )
            generator = check( node, definitions )

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


