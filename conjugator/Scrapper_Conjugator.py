import argparse
import requests
from bs4 import BeautifulSoup
import more_itertools

# see: HTML: https://api.verbix.com/conjugator/html
# see: JSON: https://api.verbix.com/conjugator/json
VERBIX_TABLE_URL = 'http://tools.verbix.com/webverbix/personal/template.htm'
VERBIX_LANG_CODES_URL = 'http://api.verbix.com/conjugator/html'
VERBIX_URL = 'http://api.verbix.com/conjugator/html?language={0}&tableurl=' \
             + VERBIX_TABLE_URL \
             + '&verb={1}'

verbixLanguageCodes = {
	"de": "deu",
	"en": "eng",
	"da": "dan",
	"es": "spa",
	"fi": "fin",
	"fr": "fra",
	"hu": "hun",
	"is": "isl",
	"it": "ita",
	"la": "lat",
	"nl": "nld",
	"no": "nob",
	"pt": "por",
	"ro": "ron",
	"ru": "rus",
	"sv": "swe"
}

titles = {
    "Indicativo" : "Indicative",
    "Presente"   : "Present",
    "Imperfecto" : "Imperfect",
    "Futuro"     : "Future",
    "Subjuntivo" : "Subjunctive",
    "Condicional": "Conditional",
    "Imperativo" : "Imperative",
    "Infinitivo" : "Infinitive",
}


# Indicative
#   Present
#   Imperfect
#   Future
#   Perfect
#   PastPerfect
#   PreviousFuture
# Subjunctive
#   Present
#   Imperfect
#   Future
#   Perfect
#   PastPerfect
#   PreviousFuture
# Conditional
#   Conditional
#   PerfectConditiontal
# Imperativo


def check_connection():
    lang = 'eng'
    verb = 'do'
    response = requests.get( VERBIX_URL.format( lang, verb ) )

    if response.status_code == 200:
        pass
    else:
        raise Exception( "Returned status code != 200: ", response.status_code )


def get_conjugations( lang, verb ):
    """Use the verbix API to return a list of all conjugations
    of a given verb/language combination

    :param str lang: Language code
    :param str verb: Verb to conjugate

    Result example:
    [
        ('Infinitive'  , None                   , None        , 'to do')
        ('Participle'  , None                   , None        , 'done')
        ('Gerund'      , None                   , None        , 'doing')
        ('Indicativo'  , 'Presente'             , 'I'         , 'do')
        ('Indicativo'  , 'Presente'             , 'you'       , 'do')
        ('Indicativo'  , 'Presente'             , 'he;she;it' , 'does')
        ('Indicativo'  , 'Presente'             , 'we'        , 'do')
        ('Indicativo'  , 'Presente'             , 'you'       , 'do')
        ('Indicativo'  , 'Presente'             , 'they'      , 'do')
        ('Indicativo'  , 'Perfecto'             , 'I'         , 'have done')
        ('Indicativo'  , 'Perfecto'             , 'you'       , 'have done')
        ('Indicativo'  , 'Perfecto'             , 'he;she;it' , 'has done')
        ('Indicativo'  , 'Perfecto'             , 'we'        , 'have done')
        ('Indicativo'  , 'Perfecto'             , 'you'       , 'have done')
        ('Indicativo'  , 'Perfecto'             , 'they'      , 'have done')
        ('Indicativo'  , 'Imperfecto'           , 'I'         , 'did')
        ('Indicativo'  , 'Imperfecto'           , 'you'       , 'did')
        ('Indicativo'  , 'Imperfecto'           , 'he;she;it' , 'did')
        ('Indicativo'  , 'Imperfecto'           , 'we'        , 'did')
        ('Indicativo'  , 'Imperfecto'           , 'you'       , 'did')
        ('Indicativo'  , 'Imperfecto'           , 'they'      , 'did')
        ('Indicativo'  , 'Pluscuamperfecto'     , 'I'         , 'had done')
        ('Indicativo'  , 'Pluscuamperfecto'     , 'you'       , 'had done')
        ('Indicativo'  , 'Pluscuamperfecto'     , 'he;she;it' , 'had done')
        ('Indicativo'  , 'Pluscuamperfecto'     , 'we'        , 'had done')
        ('Indicativo'  , 'Pluscuamperfecto'     , 'you'       , 'had done')
        ('Indicativo'  , 'Pluscuamperfecto'     , 'they'      , 'had done')
        ('Indicativo'  , 'Futuro'               , 'I'         , 'will do')
        ('Indicativo'  , 'Futuro'               , 'you'       , 'will do')
        ('Indicativo'  , 'Futuro'               , 'he;she;it' , 'will do')
        ('Indicativo'  , 'Futuro'               , 'we'        , 'will do')
        ('Indicativo'  , 'Futuro'               , 'you'       , 'will do')
        ('Indicativo'  , 'Futuro'               , 'they'      , 'will do')
        ('Indicativo'  , 'Futuro anterior'      , 'I'         , 'will have done')
        ('Indicativo'  , 'Futuro anterior'      , 'you'       , 'will have done')
        ('Indicativo'  , 'Futuro anterior'      , 'he;she;it' , 'will have done')
        ('Indicativo'  , 'Futuro anterior'      , 'we'        , 'will have done')
        ('Indicativo'  , 'Futuro anterior'      , 'you'       , 'will have done')
        ('Indicativo'  , 'Futuro anterior'      , 'they'      , 'will have done')
        ('Subjuntivo'  , 'Presente'             , 'I'         , 'do')
        ('Subjuntivo'  , 'Presente'             , 'you'       , 'do')
        ('Subjuntivo'  , 'Presente'             , 'he;she;it' , 'do')
        ('Subjuntivo'  , 'Presente'             , 'we'        , 'do')
        ('Subjuntivo'  , 'Presente'             , 'you'       , 'do')
        ('Subjuntivo'  , 'Presente'             , 'they'      , 'do')
        ('Subjuntivo'  , 'Perfecto'             , 'I'         , 'have done')
        ('Subjuntivo'  , 'Perfecto'             , 'you'       , 'have done')
        ('Subjuntivo'  , 'Perfecto'             , 'he;she;it' , 'have done')
        ('Subjuntivo'  , 'Perfecto'             , 'we'        , 'have done')
        ('Subjuntivo'  , 'Perfecto'             , 'you'       , 'have done')
        ('Subjuntivo'  , 'Perfecto'             , 'they'      , 'have done')
        ('Condicional' , 'Condicional'          , 'I'         , 'would do')
        ('Condicional' , 'Condicional'          , 'you'       , 'would do')
        ('Condicional' , 'Condicional'          , 'he;she;it' , 'would do')
        ('Condicional' , 'Condicional'          , 'we'        , 'would do')
        ('Condicional' , 'Condicional'          , 'you'       , 'would do')
        ('Condicional' , 'Condicional'          , 'they'      , 'would do')
        ('Condicional' , 'Condicional perfecto' , 'I'         , 'would have done')
        ('Condicional' , 'Condicional perfecto' , 'you'       , 'would have done')
        ('Condicional' , 'Condicional perfecto' , 'he;she;it' , 'would have done')
        ('Condicional' , 'Condicional perfecto' , 'we'        , 'would have done')
        ('Condicional' , 'Condicional perfecto' , 'you'       , 'would have done')
        ('Condicional' , 'Condicional perfecto' , 'they'      , 'would have done')
        ('Imperativo'  , ''                     , 'you'       , 'do')
        ('Imperativo'  , ''                     , 'we'        , "Let's do")
        ('Imperativo'  , ''                     , 'you'       , 'do')
    ]
    """
    result = []

    # Make http request
    try:
        response = requests.get( VERBIX_URL.format( lang, verb ) )

    except requests.exceptions.RequestException as e:
        print( "Exception connecting to Verbix API" )
        print( e )
        return set( [ ] )

    html_string = response.text

    # Parse response using beautiful soup
    soup = BeautifulSoup( html_string, "html5lib" )

    # table
    #   tr
    #     td
    #       b
    #         Infinitivo
    #       span
    #         span class="normal"
    #           .text -> ...
    #       b
    #         Participio
    #       span
    #         span class="irregular"
    #           .text -> ...
    #       b
    #         Gerundio
    #         span class="normal"
    #           .text -> ...
    #   tr
    #     td
    #       b
    #        .text = "Indicativo"
    #       table class="verbtense"
    #         tr
    #           td
    #             b
    #               .text = "Presente"
    #             table
    #               tr
    #                 td
    #                   span class="pronoun"
    #                     .text -> term
    #                   span class="normal"
    #                     .text -> term

    table_main = soup.find( 'table', attrs={ 'border': "1" })

    trs_table_main = table_main.tbody.find_all('tr', recursive=False)
    tr1 = trs_table_main[0]

    for b in tr1.find('td').find_all('b'):
        if b.text.strip() == 'Infinitivo:':
            span = b.find_next('span')
            if span:
                Infinitive = span.text
                result.append( ("Infinitive", None, None, Infinitive) )

        elif b.text.strip() == 'Participio:':
            span = b.find_next('span')
            if span:
                Participle = span.text
                result.append( ("Participle", None, None, Participle) )

        elif b.text.strip() == 'Gerundio:':
            span = b.find_next('span')
            if span:
                Gerund = span.text
                result.append( ("Gerund", None, None, Gerund) )

    # Sections
    # Verb forms
    tr_rest = trs_table_main[1:]

    for tr_tr in more_itertools.sliced( tr_rest, 2 ):
        if len(tr_tr) == 2:
            (tr_with_title, tr_with_data) = tr_tr

            for td_section_title, td_section_data in zip( tr_with_title.find_all('td', recursive=False), tr_with_data.find_all('td', recursive=False) ):
                # title
                section_title = td_section_title.text

                # terms by form
                table_tenses = td_section_data.find_all('table', class_="verbtense")

                for table_tense in table_tenses:
                    b_title = table_tense.parent.find('b')

                    if b_title:
                        # title
                        title = b_title.text.strip()

                        for tr in table_tense.find_all('tr'):
                            td_pronoun, td_term = tr.find_all('td')

                            # pronoun
                            pronoun = td_pronoun.text.strip()

                            # split "he;she;it" to ['he', 'she', 'it']
                            pronouns = pronoun.split(';')
                            pronouns = map(str.strip, pronouns)

                            # term
                            term    = td_term.text.strip()

                            # result
                            for pronoun in pronouns:
                                result.append( (section_title, title, pronoun, term) )

    return result

