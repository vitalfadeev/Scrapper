from collections import defaultdict
import more_itertools
import Scrapper_IxiooAPI
from wiktionary.Scrapper_Wiktionary_WikitextParser import Section, Header, Template, Li, Link, String, Container
from wiktionary.en import Scrapper_Wiktionary_EN_Templates



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
        section = node.sections.get( title, None )

        if section is not None:
            # do next check
            yield from check( page, explanation, section, defs )


# read block from {{trans-top}} to {{trans-bottom}}
def trans_top_reader( lexems, start_element ):
    reader = iter( lexems )
    for e in lexems:
        if e is reader:
            break

    next( reader, None )

    for e in reader:
        if isinstance( e, Template ) and e.name == 'trans-bottom':
            break
        else:
            yield e

def in_trans_top_by_sense( page, explanation, context, definitions ):
    # get translations
    # {{trans-top|...}}
    # *Abkhaz: {{t | ab | ацгә}}
    # *Acehnese: {{t | ace | mië}}
    # *Adyghe: {{t | ady | кӏэтыу}}
    #
    # if many explanations
    #   1. find section 'Translations'. (context)
    #   2. get all senses
    #       find all {{trans-top|...}}
    #       get first arg. it is sense
    #       sense-raw to sense-txt
    #       save to cache.  senses[ sense ] = element
    #   3. pks match senses + explanations
    #   4. get matched sense. and related container
    #   5. in container find all li
    #      for each li:
    #         get first word. it is language
    #         if language == expected lang
    #            get word
    #   6. save parsed {{trans-top|...}} to cache. for use with other languages
    #      section.trans_top_by_sense[ sense ][ language ] = Container
    #
    # if single explanation
    #   1. find section 'Translations'. (context)
    #   2. find all {{trans-top|...}}
    #   3. get all

    node = context
    section = context
    expect_langs = definitions.keys()

    # if many explanations
    if len( page.explanations ) > 1:
        # 1. we in section 'Translations'. (context)
        # 2. get all senses. (for use in matching)
        #     find all {{trans-top|...}}
        #     get first arg. it is sense
        #     sense-raw to sense-txt
        #     save to cache.  senses[ sense ] = element
        by_sense = {}

        for t in node.find_lexem( recursive=False ):
            if isinstance( t, Template ):
                if t.name == 'trans-top':
                    # get sense
                    sense_raw = t.arg(0, raw=True)
                    if sense_raw:
                        # sense-raw to sense-txt
                        sense_txt = page.text_by_raw[ sense_raw ]
                        by_sense[ sense_txt ] = t
        # we have all senses!

        if by_sense:
            pass

        # 3. pks match senses + explanations
        if by_sense and section.by_sense:
            # prepare pks match
            explanations = list( page.explanation_by_sense.keys() )
            section_senses = list( section.by_sense.keys() )

            # do pks match
            if explanations and section_senses:
                matches = Scrapper_IxiooAPI.Match_List_PKS_With_Lists_Of_PKS( explanations, section_senses )

                # cache
                section.sense_matches = dict( matches )

            else:
                # if no senses
                section.sense_matches = { }

        matched_lexemes_container = None

        # 4. get matched sense. and related container
        if section.sense_matches:
            e_sense = explanation.sense_txt
            t_sense = section.sense_matches.get( e_sense, None )

            if t_sense:
                # find matched lexemes
                matched_lexemes_container = section.by_sense[ t_sense ]

        # 5. in container find all li
        #    for each li:
        #       get first word. it is language
        #       if language == expected lang
        #          get word
        #matched_lexemes_container = next( filter( lambda x: isinstance(x, Template) and x.name == 'trans-top', section.lexems ), None )
        if matched_lexemes_container:
            # extract words
            for li in trans_top_reader( section.lexems, matched_lexemes_container ):
                if isinstance( li, Li ):
                    # get first word. it is language
                    language_raw = li.childs[ 0 ].raw
                    language = language_raw.strip( ': \n' ).lower()

                    if language in expect_langs:
                        yield from check( page, explanation, li, definitions[ language ] )

    # if sungle explanation
    if len( page.explanations ) == 1:
        for li in section.lexems:
            if isinstance( li, Li ):
                #    for each li:
                #       get first word. it is language
                language_raw = li.childs[ 0 ].raw
                language = language_raw.strip( ': \n' ).lower()

                if language in expect_langs:
                    yield from check( page, explanation, li, definitions[ language ] )
            break


def if_explanation( page, explanation, context, definitions ):
    if hasattr( context, 'is_explanation' ) and context.is_explanation:
        yield from check( page, explanation, context, definitions )


def text_contain( page, explanation, context, definitions ):
    for text in definitions:
        if repr(context).find( text ) != -1:
            yield True


def in_template( page, explanation, context, definitions: dict ):
    for t in context.find_lexem( recursive=True ):
        if isinstance(t, Template):
            defs = definitions.get( t.name, None )
            if defs is not None:
                yield from check( page, explanation, t, defs )


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


# def if_single_explanation( page, explanation, context, definitions ):
#     if len( page.explanations ) == 1:
#         yield from check( page, explanation, context, definitions )
#
#
# def if_many_explanations( page, explanation, context, definitions ):
#     if len( page.explanations ) > 1:
#         yield from check( page, explanation, context, definitions )


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
        if parent.is_explanation is False:
            yield from check( page, explanation, parent, definitions )

        parent = parent.parent


def in_examples( page, explanation, context, definitions ):
    for child in context:
        if child.is_example:
            yield from check( page, explanation, child, definitions )


def get_li_senses_en( page, section ):
    """
    search: * {{sense|...}}
    return [ ('sentence1', lexemes_container1), ('sentence2', lexemes_container2),) ]
    """
    for lexem in section.lexems:
        if isinstance( lexem, Li ):
            li = lexem
            for t in lexem.find_objects( Template, recursive=False ):
                if t.name == 'sense':
                    raw = t.arg( 0, raw=True )
                    txt = page.text_by_raw[ raw ]
                    yield (txt, li)

def in_li_by_sense_en( page, explanation, context, definitions ):
    """
    # extract senses
    # if single explaanation:
    #   get all from section
    #
    # if many explanations:
    #   get_senses: {           # extract senses. senes[ sense ] = [ lexem, lexem ]
    #       in_li: {
    #           in_template: {
    #               'sense': {
    #                   in_arg: { 0 }
    #               }
    #           }
    #       }
    #   },
    #   pks match
    #     all explanations + all section_senses
    #     cache matches
    #
    #   here have: section_senses, explanation sense, matched pairs
    #   match:
    #     have section_senses + explanation_sense
    #     sense
    """
    section = context

    # if single explanation
    if len( page.explanations ) == 1:
        # extract words
        yield from check( page, explanation, section, definitions )

    # if many explanations
    elif len( page.explanations ) > 1:
        # check cached
        if section.sense_matches is None:
            # extract senses
            section.by_sense = dict( get_li_senses_en( page, section ) )
            # we have all senses!

            # prepare pks match
            explanations = list( page.explanation_by_sense.keys() )
            section_senses = list( section.by_sense.keys() )

            # do pks match
            if explanations and section_senses:
                matches = Scrapper_IxiooAPI.Match_List_PKS_With_Lists_Of_PKS( explanations, section_senses )

                # cache
                section.sense_matches = dict( matches )

            else:
                # if no senses
                section.sense_matches = {}

        #
        e_sense = explanation.sense_txt
        s_sense = section.sense_matches.get( e_sense, None )

        if s_sense:
            # find matched lexemes
            matched_lexemes_container = section.by_sense[ s_sense ]

            # extract words
            yield from check( page, explanation, matched_lexemes_container, definitions )


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
    (s, p, is_uncountable) = next( en_noun( t, label ) )

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
        # if name == 'SeeAlso':
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
        defs.update( to_append )

    return defs
