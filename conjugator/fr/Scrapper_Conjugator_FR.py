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
        if h4.text.strip().lower() == "infinitif":
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
                        if "graytxt" in i_el.attrs[ "class" ]:
                            pronoun_el = li.find( "i", class_ = "graytxt" )
                            pronoun = pronoun_el.text if pronoun_el else ""
                        else:
                            verb += i_el.text

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

    index = defaultdict( str )

    for x in verbs_group:
        if x[0]:
            xs1 = x[1] if x[1] else ""
            index[ x[0] ] = xs1

    if pronoun == 'je':
        p = index[ 'nous' ]
    elif pronoun == "j'":
        p = index[ 'nous' ]
    elif pronoun == "j'/je":
        p = index[ 'nous' ]
    elif pronoun == 'tu':
        p = index[ 'vous' ]
    elif pronoun == 'il':
        p = index[ 'ils' ]
    elif pronoun == 'elle':
        p = index[ 'elles' ]

    elif pronoun == 'nous':
        s = index[ 'je' ]
    elif pronoun == 'vous':
        s = index[ 'tu' ]
    elif pronoun == 'ils':
        s = index[ 'il' ]
    elif pronoun == 'elles':
        s = index[ 'elle' ]

    return (s, p)


def decode_conj_tense( tense, pronoun, verb ):
    conj_map = {
        "Indicatif Présent"                 : (0, 1, 0),
        "Indicatif Imparfait"               : (1, 0, 0),
        "Indicatif Futur"                   : (0, 0, 1),
        "Passé simple"                      : (1, 0, 0),
        "Passé composé"                     : (1, 0, 0),
        "Indicatif Plus-que-parfait"        : (1, 0, 0),
        "Passé antérieur"                   : (1, 0, 0),
        "Futur antérieur"                   : (0, 0, 1),
        "Présent"                           : (0, 1, 0),
        "Imparfait"                         : (1, 0, 0),
        "Plus-que-parfait"                  : (1, 0, 0),
        "Passé"                             : (1, 0, 0),
        "Conditionnel Présent"              : (0, 1, 0),
        "Conditionnel Passé première forme" : (1, 0, 0),
        "Conditionnel Passé deuxiéme forme" : (1, 0, 0),
        "Participe Présent"                 : (0, 1, 0),
        "Participe Passé composé"           : (1, 0, 0),
        "Participe Passé"                   : (1, 0, 0),
        "Impératif Présent"                 : (0, 1, 0),
        "Impératif Passé"                   : (1, 0, 0),
        "Infinitif Présent"                 : (0, 1, 0),
        "Infinitif Passé"                   : (1, 0, 0),
        "Indicatif Passé simple"            : (1, 0, 0),
        "Indicatif Passé composé"           : (1, 0, 0),
        "Indicatif Passé antérieur"         : (1, 0, 0),
        "Indicatif Futur antérieur"         : (0, 0, 1),
        "Subjonctif Présent"                : (0, 1, 0),
        "Subjonctif Imparfait"              : (1, 0, 0),
        "Subjonctif Plus-que-parfait"       : (1, 0, 0),
        "Subjonctif Passé"                  : (1, 0, 0),
    }

    key = tense

    return conj_map[ key ]


def decode_conj_amount( tense, pronoun, verb ):
    amount_map = {
        "j'/je"     : (1, 0),
        "j'"        : (1, 0),
        'je'        : (1, 0),
        'tu'        : (1, 0),
        'il'        : (1, 0),
        'elle'      : (1, 0),
        'nous'      : (0, 1), # we
        'vous'      : (0, 1), # he
        'ils'       : (0, 1), # they
        'elles'     : (0, 1), # they
        'masc.sg.:' : (1, 0),
        'masc.pl.:' : (0, 1),
        'fém.sg.:'  : (1, 0),
        'fém.pl.:'  : (0, 1),
        ''          : (0, 0),
    }

    return amount_map[ pronoun ]


def decode_gender( tense, pronoun, verb ):
    gender_map = {
        'masc.sg.:' : (1, 0),
        'masc.pl.:' : (1, 0),
        'fém.sg.:'  : (9, 1),
        'fém.pl.:'  : (0, 1),
    }

    return gender_map.get( pronoun, (None, None) )


def get_label_type( page, tense, infinitive, pronoun ):
    # Verb_To_do_You_Indicative Perfect
    s = "Verb" + '_' + proper( page.label) + '_' + proper( pronoun ) + '_' + tense
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

            # IsMale, IsFeminine
            m, f = decode_gender( tense, pronoun, verb )

            if m == 1:
                item.IsMale = True

            if f == 1:
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

