import argparse
import requests
from bs4 import BeautifulSoup
import sys

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
    "Indicativo": "Indicative",
    #   Presente   -> Present
    #   Imperfecto -> Imperfect
    #   Futuro     -> Future
    "Subjuntivo": "Subjunctive",
    #   Presente   -> Present
    #   Imperfecto -> Imperfect
    #   Futuro     -> Future
    "Condicional": "Conditional",
    #   Condicional -> Conditional
    "Imperativo":  "Imperative",
    #   (empty)
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
    """

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

    table_tenses = table_main.find_all('table', class_="verbtense")

    for table_tense in table_tenses:
        b_title = table_tense.parent.find('b')

        if b_title:
            title = b_title.text.strip()

            for tr in table_tense.find_all('tr'):
                span_pronoun = tr.find('span', class_="pronoun")
                span_normal  = tr.find('span', class_="normal")

                if span_pronoun:
                    pronoun = span_pronoun.text.strip()
                else:
                    pronoun = ''

                if span_normal:
                    normal = span_normal.text.strip()
                else:
                    normal = ''

                print( (title, pronoun, normal) )

    all_verbs = set( [ ] )

    return all_verbs

