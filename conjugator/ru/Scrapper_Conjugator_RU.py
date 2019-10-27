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
        if a.attrs.get("tooltip", "").strip().lower() == "existing infinitive":
            return a.text
        if a.attrs.get("tooltip", "").strip().lower() == "unknown infinitive":
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

                    # <hr class="sex musculine" noshade="">
                    # <hr class="sex feminine" noshade="">
                    is_musculine = li.find( "hr", attrs={"class": "musculine"}, recursive=True )
                    is_feminine  = li.find( "hr", attrs={"class": "feminine"} )

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

                    verbs[ tense ].append( ( pronoun, verb, is_musculine, is_feminine ) )

    return verbs


def get_single_plural_variant( tense, pronoun, verb, verbs_group ):
    # I - we
    # you - you
    # he/she/it - they
    s = None
    p = None

    index = defaultdict( str )

    for x in verbs_group:
        if x[0]:
            xs1 = x[1] if x[1] else ""
            index[ x[0] ] = xs1

    if pronoun == 'я':
        p = index[ 'мы' ]
    elif pronoun == 'я/ты/он':
        p = index[ 'мы' ]
    elif pronoun == 'я/ты/она':
        p = index[ 'мы' ]
    elif pronoun == 'ты':
        p = index[ 'вы' ]
    elif pronoun == 'он/она/оно':
        p = index[ 'они' ]
    elif pronoun == 'оно':
        p = index[ 'они' ]

    elif pronoun == 'мы/вы/они':
        s = index[ 'я' ]
    elif pronoun == 'мы':
        s = index[ 'я' ]
    elif pronoun == 'вы':
        s = index[ 'ты' ]
    elif pronoun == 'они':
        s = index[ 'он/она/оно' ]

    return (s, p)


def decode_conj_tense( tense, pronoun, verb ):
    conj_map = {
        "настоящее"                          : (0, 1, 0),
        "прошедшее"                          : (1, 0, 0),
        "будущее"                            : (0, 0, 1),
        "Изъявительное наклонение настоящее" : (0, 1, 0),
        "Изъявительное наклонение прошедшее" : (1, 0, 0),
        "Изъявительное наклонение будущее"   : (0, 0, 1),
        "Деепричастие настоящее"             : (0, 1, 0),
        "Деепричастие прошедшее"             : (1, 0, 0),
        "Причастие настоящее"                : (0, 1, 0),
        "Причастие прошедшее"                : (1, 0, 0),
        "Императив"                          : (0, 1, 0),
        "Сослагательное наклонение"          : (0, 1, 0),
        "Причастие активный залог"           : (0, 1, 0),
        "Причастие пассивный залог"          : (0, 1, 0),
    }

    key = tense

    return conj_map[ key ]


def decode_conj_amount( tense, pronoun, verb ):
    amount_map = {
        'я/ты/он'   : (1, 0),
        'я/ты/она'  : (1, 0),
        'оно'       : (1, 0),
        'я'         : (1, 0),
        'ты'        : (1, 0),
        'он/она/оно': (1, 0),
        'мы/вы/они' : (0, 1),
        'мы'        : (0, 1),
        'вы'        : (0, 1),
        'они'       : (0, 1),
        ''          : (0, 0),
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
    for (tense, verbs_group) in verbs.items():
        for pronoun, verb, is_musculine, is_feminine in verbs_group:                           # for each verb
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
            if is_musculine:
                item.IsMale = True

            if is_feminine:
                item.IsFeminine = True

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

