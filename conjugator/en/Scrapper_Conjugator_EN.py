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
    for h4 in soup.select( 'h4' ):
        if h4.text.strip().lower() == "infinitive":
            return h4.find_parent().find_parent().find( 'li' ).text


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

    for word_wrap_row in soup.select( "div.word-wrap-row" ):
        for blue_box_box_wrap in word_wrap_row.select( "div.blue-box-wrap" ):
            h = blue_box_box_wrap.attrs.get( "mobile-title", None )

            for ul in blue_box_box_wrap.select( "ul.wrap-verbs-listing" ):
                for li in ul.select( "li" ):
                    t1 = li.find( "i", class_="graytxt" )
                    t2 = li.find( "i", class_="auxgraytxt" )
                    if t2 is None:
                        t2 = li.find( "i", class_="particletxt" )
                    t3 = li.find( "i", class_="verbtxt" )

                    header = h.strip() if h is not None else None
                    s1 = t1.text.strip() if t1 is not None else ''
                    s2 = t2.text.strip() if t2 is not None else ''
                    s3 = t3.text.strip() if t3 is not None else ''

                    verbs[ header ].append( ( s1, s2, s3 ) )

    return verbs


def get_single_plural_variant( header, s1, s2, s3, verbs_group ):
    # I - we
    # you - you
    # he/she/it - they
    s = None
    p = None

    index = defaultdict( None )

    for x in verbs_group:
        if x[0]:
            xs1 = x[1] if x[1] else ""
            xs2 = x[2] if x[2] else ""
            index[ x[0] ] = xs1 + ' ' + xs2

    if s1 == 'I':
        p = index[ 'we' ]
    elif s1 == 'you':
        s = index[ 'you' ]
        p = index[ 'you' ]
    elif s1 == 'he/she/it':
        p = index[ 'they' ]

    elif s1 == 'we':
        s = index[ 'I' ]
    elif s1 == 'you':
        s = index[ 'you' ]
        p = index[ 'you' ]
    elif s1 == 'they':
        s = index[ 'he/she/it' ]

    return (s, p)


def decode_conj_tense( header, pronoun, participle, verb ):
    conj_map = {
        "Simple present": (0, 1, 0),
        "Indicative Present continuous": (0, 1, 0),
        "Indicative Present perfect": (0, 1, 0),
        "Indicative Future": (0, 0, 1),
        "Indicative Present": (0, 1, 0),
        "Indicative Preterite": (0, 1, 0),
        "Indicative Future perfect": (0, 0, 1),
        "Indicative Past continous": (1, 0, 0),
        "Indicative Past perfect": (1, 0, 0),
        "Indicative Future continuous": (0, 0, 1),
        "Indicative Present perfect continuous": (0, 1, 0),
        "Indicative Past perfect continuous": (1, 0, 0),
        "Indicative Future perfect continuous": (0, 0, 1),
        # "Imperative": (0, 1, 0),
        "Participle Present": (0, 1, 0),
        "Participle Past": (1, 0, 0),
        # "Infinitive": (0, 1, 0),
        "Perfect participle": (0, 1, 0),

        "Simple past": (1, 0, 0),
        "Present perfect simple": (0, 1, 0),
        "Present progressive/continuous": (0, 1 ,0),
        "Past progressive/continuous": (1, 0, 0),
        "Present perfect progressive/continuous": (0, 1, 0),
        "Past perfect": (1, 0, 0),
        "Past perfect progressive/continuous": (1, 0, 0),
        "Future": (0, 0, 1),
        "Future progressive/continuous": (0, 0, 1),
        "Future perfect": (0, 0, 1),
        "Future perfect continuous": (0, 0, 1),
        "Imperative": (0, 1, 0),
        "Infinitive": (0, 1, 0),
        "Present Participle": (0, 1, 0),
        "Past Participle": (1, 0, 0),
        "Perfect participle ": (0, 1, 0),
        "Indicative Present ": (0, 1, 0),
    } 

    return conj_map[ header ]


def decode_conj_amount( header, s1, s2, s3 ):
    amount_map = {
        'I': (1, 0),
        'you': (1, 1),
        'he/she/it': (1, 0),
        'we': (0, 1),
        # 'you': (0, 1),
        'they': (0, 1),
        '': (0, 0),
    }

    return amount_map[ s1 ]


def get_label_type( page, header, infinitive, pronoun ):
    # Verb_To_do_You_Indicative Perfect
    s = "Verb" + '_' + proper( infinitive ) + '_' + proper( pronoun ) + '_' + header
    s = s.replace( ' ', '_' )
    return s


def get_explanation_txt( page, header, infinitive, pronoun ):
    # Verb,  to do , you, indicative perfect
    s = "Verb" + ', ' + infinitive + ', ' + pronoun + ', ' + header
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
    for header, verbs_group in verbs.items():
        for pronoun, participle, verb in verbs_group:                           # for each verb
            #
            item = ConjugationsItem()

            # Past, Present, Future
            is_past, is_present, is_future = decode_conj_tense( header, pronoun, participle, verb )

            if is_past:
                item.IsVerbPast = True

            if is_present:
                item.IsVerbPresent = True

            if is_future:
                item.IsVerbFutur = True

            # IsSingle, IsPlural
            is_single, is_plural = decode_conj_amount( header, pronoun, participle, verb )

            if is_single:
                item.IsSingle = True

            if is_plural:
                item.IsPlural = True

            # SingleVariant, PluralVariant
            sv, pv = get_single_plural_variant( header, pronoun, participle, verb, verbs_group )
            item.SingleVariant = sv
            item.PluralVariant = pv

            #
            item.LabelName = (participle + ' ' + verb).strip()

            # Type
            item.Type = 'Verb'

            # AlternativeFormsOther
            item.AlternativeFormsOther.append( infinitive )

            # OtherwiseRelated
            ovs = [ ]

            for h, vg in verbs.items():
                for v in vg:
                    ov = (v[1] + ' ' + v[2]).strip()
                    if ov != item.LabelName:   # filter self
                        ovs.append( ov )

            ovs = unique( ovs )

            item.OtherwiseRelated.extend( ovs )

            # Explaination
            # Verb , INFINITIVE , subject , tense-name
            item.ExplainationTxt = get_explanation_txt( page, header, infinitive, pronoun )

            # LabelType
            item.LabelType = get_label_type( page, header, infinitive, pronoun )

            #
            item.LanguageCode = "en"
            item.PK = item.LanguageCode + '"§"' + item.LabelName + '"§"' + item.LabelType + '"§"' + str( i )

            #
            items.append( item )

            #
            i += 1

    return items

