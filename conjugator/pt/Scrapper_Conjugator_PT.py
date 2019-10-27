# verb conjugations scrap
#
# 1. get list of verb from https://cooljugator.com/fr/list/all
# 2. get conjugations from http://conjugueur.reverso.net/regles-conjugaison-modeles-francais.html
# 3. parse
# 4. save

# 1. get list of verb from https://cooljugator.com/fr/list/all
#    ~ 30 000 items
#    html
#      ul
#        li class="item"
#          a
#            .text
import logging
from collections import defaultdict

import bs4

from Scrapper_Helpers import unique, proper
from conjugator.Scrapper_Conjugations_Item import ConjugationsItem
from conjugator.Scrapper_Conjugator import Page

log = logging.getLogger(__name__)


def get_infinitive( page, soup ):
    for a in soup.select( 'a#ch_lblVerb' ):
        if a.attrs.get( "tooltip", "" ).strip().lower() == "existing infinitive":
            return a.text
        if a.attrs.get( "tooltip", "" ).strip().lower() == "unknown infinitive":
            log.warning( "Unknown infinitive: %s", a.text )
            return a.text


def get_verbs( page: Page, soup ) -> defaultdict :
    """
    Scrap verbs from page

    Args:
        page (Page):            Page instance
        soup (BeautyfullSoup):  BeautyfullSoup instance

    Returns:
        dict[ INDICATIVE ] = [('I', None, 'did'), ('you', None, 'did'), ...]
    """
    verbs = defaultdict( list )
    form = ""

    for word_wrap_row in soup.select( "div.word-wrap-row" ):
        # form
        word_wrap_title = word_wrap_row.find( "div", class_="word-wrap-title" )

        if word_wrap_title:
            form = word_wrap_title.find( "h4" ).text
            if form is None:
                form = ''

        # tenses
        for blue_box_box_wrap in word_wrap_row.select( "div.blue-box-wrap" ):
            # tense
            h = blue_box_box_wrap.attrs.get( "mobile-title", None )
            tense = h.strip() if h is not None else None

            for ul in blue_box_box_wrap.select( "ul.wrap-verbs-listing" ):
                for li in ul.select( "li" ):
                    pronoun_el = None
                    pronoun = ""
                    verb = ""

                    for i_el in li.select( "i" ):
                        # skip transliteration
                        if i_el.find_parents( attrs={"class": "transliteration"} ):
                            continue

                        # skip transliteration 2
                        if i_el.find_parents( "div", class_="transliteration" ):
                            continue

                        # skip parts on one
                        if i_el.find_parents( "i", attrs={"h": "1"} ):
                            continue

                        #
                        if "graytxt" in i_el.attrs.get( "class" , []):
                            pronoun = i_el.text
                        else:
                            # verbtxt, maroontxt
                            verb += ' ' + i_el.text

                    pronoun = pronoun.strip().lstrip('(').rstrip(')').strip()
                    verb = verb.strip().lstrip('(').rstrip(')').strip()

                    verbs[ tense ].append( ( pronoun, verb ) )

    return verbs


def get_single_plural_variant( tense, pronoun, verb, verbs_group ):
    # I - we
    # you - you
    # he/she/it - they
    s = None
    p = None

    index = defaultdict( None )

    for x in verbs_group:
        if x[0]:
            xs1 = x[1] if x[1] else ""
            index[ x[0] ] = xs1

    if pronoun == 'eu':
        p = index[ 'nós' ]
    elif pronoun == 'tu':
        p = index[ 'vós' ]
    elif pronoun == 'ele/ela/você':
        p = index[ 'eles/elas/vocês' ]

    elif pronoun == 'nós':
        s = index[ 'eu' ]
    elif pronoun == 'vós':
        s = index[ 'tu' ]
    elif pronoun == 'eles/elas/vocês':
        s = index[ 'ele/ela/você' ]

    return (s, p)


def decode_conj_tense( tense, pronoun, verb ):
    conj_map = {
        "indicativo presente"                                          : (0, 1, 0),
        "indicativo pretérito imperfeito"                              : (1, 0, 0),
        "indicativo pretérito mais-que-perfeito simples"               : (1, 0, 0),
        "indicativo pretérito perfeito composto"                       : (1, 0, 0),
        "indicativo pretérito perfeito simples"                        : (1, 0, 0),
        "indicativo pretérito mais-que-perfeito anterior"              : (1, 0, 0),
        "indicativo futuro do presente simples"                        : (0, 0, 1),
        "indicativo futuro do presente composto"                       : (0, 0, 1),
        "condicional futuro do pretérito simples"                      : (0, 1, 0),
        "condicional futuro do pretérito composto"                     : (1, 0, 0),
        "conjuntivo / subjuntivo presente"                             : (0, 1, 0),
        "conjuntivo / subjuntivo pretérito imperfeito"                 : (1, 0, 0),
        "conjuntivo / subjuntivo futuro simples"                       : (0, 0, 1),
        "conjuntivo / subjuntivo pretérito perfeito"                   : (1, 0, 0),
        "conjuntivo / subjuntivo pretérito mais-que-perfeito"          : (1, 0, 0),
        "conjuntivo / subjuntivo futuro composto"                      : (0, 0, 1),
        "infinitivo pessoal presente"                                  : (0, 1, 0),
        "infinitivo pessoal pretérito"                                 : (1, 0, 0),
        "imperativo afirmativo"                                        : (0, 1, 0),
        "imperativo negativo"                                          : (0, 1, 0),
        "indicativo pretérito perfeito"                                : (1, 0, 0),
        "indicativo pretérito mais-que-perfeito"                       : (1, 0, 0),
        "indicativo pretérito mais-que-perfeito composto"              : (1, 0, 0),
        "conjuntivo / subjuntivo pretérito mais-que-perfeito composto" : (1, 0, 0),
        "conjuntivo / subjuntivo futuro"                               : (0, 0, 1),
        "gerúndio"                                                     : (0, 1, 0),
        "infinitivo"                                                   : (0, 1, 0),
        "imperativo"                                                   : (0, 1, 0),
        "particípio"                                                   : (0, 1, 0),
    }

    return conj_map[ tense.lower() ]


def decode_conj_amount( tense, pronoun, verb ):
    amount_map = {
        'eu'               : (1, 0),
        'tu'               : (1, 0),
        'ele/ela/você'     : (1, 0),
        'nós'              : (0, 1),
        'vós'              : (0, 1),
        'eles/elas/vocês'  : (0, 1),
        ''                 : (0, 0),
    }

    return amount_map[ pronoun ]


def get_label_type( page, tense, infinitive, pronoun ):
    # Verb_To_do_You_Indicative Perfect
    s = "Verb" + '_' + proper( infinitive ) + '_' + proper( pronoun ) + '_' + tense
    s = s.replace( ' ', '_' )
    return s


def get_explanation_txt( page, tense, infinitive, pronoun ):
    # Verb,  to do , you, indicative perfect
    s = "Verb" + ', ' + infinitive + ', ' + pronoun + ', ' + tense
    return s


def scrap( page: Page ):
    items = []

    #
    soup = bs4.BeautifulSoup( page.text, 'html.parser' )

    # infinitive
    infinitive = get_infinitive( page, soup )

    # get verbs
    verbs = get_verbs( page, soup )

    i = 0

    #
    for tense, verbs_group in verbs.items():
        for pronoun, verb in verbs_group:                           # for each verb
            #
            item = ConjugationsItem()

            # Past, Present, Future
            is_past, is_present, is_future = decode_conj_tense( tense, pronoun, verb )

            if is_past:
                item.IsVerbPast = True

            if is_present:
                item.IsVerbPresent = True

            if is_future:
                item.IsVerbFutur = True

            # IsSingle, IsPlural
            is_single, is_plural = decode_conj_amount( tense, pronoun, verb )

            if is_single:
                item.IsSingle = True

            if is_plural:
                item.IsPlural = True

            # SingleVariant, PluralVariant
            sv, pv = get_single_plural_variant( tense, pronoun, verb, verbs_group )
            item.SingleVariant = sv
            item.PluralVariant = pv

            #
            item.LabelName = verb.strip()

            # Type
            item.Type = 'Verb'

            # AlternativeFormsOther
            item.AlternativeFormsOther.append( infinitive )

            # OtherwiseRelated
            ovs = [ ]

            for h, vg in verbs.items():
                for v in vg:
                    ov = v[1].strip()
                    if ov != item.LabelName:   # filter self
                        ovs.append( ov )

            ovs = unique( ovs )

            item.OtherwiseRelated.extend( ovs )

            # Explaination
            # Verb , INFINITIVE , subject , tense-name
            item.ExplainationTxt = get_explanation_txt( page, tense, infinitive, pronoun )

            # LabelType
            item.LabelType = get_label_type( page, tense, infinitive, pronoun )

            #
            item.LanguageCode = page.lang
            item.PK = item.LanguageCode + '§' + item.LabelName + '§' + item.LabelType + '§' + str( i )

            #
            items.append( item )

            #
            i += 1

    return items

