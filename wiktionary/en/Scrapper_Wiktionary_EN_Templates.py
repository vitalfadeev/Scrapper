import itertools
import typing
from ..Scrapper_Wiktionary_WikitextParser import Template


TRANSLATION_LANGS = {
    'abkhaz'                 : 'ab',
    'acehnese'               : 'ace',
    'adyghe'                 : 'ady',
    'afrikaans'              : 'af',
    'ainu'                   : 'ain',
    'akan'                   : 'ak',
    'albanian'               : 'sq',
    'alemannic german'       : 'gsw',
    'amharic'                : 'am',
    'ancient'                : 'grc',
    'arabic'                 : 'ar',
    'armenian'               : 'hy',
    'aromanian'              : 'rup',
    'assamese'               : 'as',
    'asturian'               : 'ast',
    'avar'                   : 'av',
    'aymara'                 : 'ay',
    'azerbaijani'            : 'az',
    'bakung'                 : 'xkl',
    'baluchi'                : 'bal',
    'bambara'                : 'bm',
    'bandjalang'             : 'bdy',
    'bashkir'                : 'ba',
    'basque'                 : 'eu',
    'bau bidayuh'            : 'sne',
    'bavarian'               : 'bar',
    'belait'                 : 'beg',
    'belarusian'             : 'be',
    'bengali'                : 'bn',
    'bikol central'          : 'bcl',
    'blackfoot'              : 'bla',
    'blin'                   : 'byn',
    'bole'                   : 'bol',
    'breton'                 : 'br',
    'brunei malay'           : 'kxd',
    'buginese'               : 'bug',
    'bulgarian'              : 'bg',
    'burmese'                : 'my',
    'buryat'                 : 'bua',
    'cantonese'              : 'yue',
    'catalan'                : 'ca',
    'cebuano'                : 'ceb',
    'central atlas tamazight': 'tzm',
    'central dusun'          : 'dtp',
    'central melanau'        : 'mel',
    'chagatai'               : 'chg',
    'chamicuro'              : 'ccc',
    'chechen'                : 'ce',
    'chepang'                : 'cdm',
    'cherokee'               : 'chr',
    'chichewa'               : 'ny',
    'chukchi'                : 'ckt',
    'chuukese'               : 'chk',
    'chuvash'                : 'cv',
    'classical'              : 'nci',
    'coptic'                 : 'cop',
    'cornish'                : 'kw',
    'cree'                   : 'cr',
    'crimean tatar'          : 'crh',
    'cyrillic'               : 'sh',
    'czech'                  : 'cs',
    'danish'                 : 'da',
    'dargwa'                 : 'dar',
    'dhivehi'                : 'dv',
    'dhuwal'                 : 'dwu',
    'drung'                  : 'duu',
    'dungan'                 : 'dng',
    'dutch'                  : 'nl',
    'dzongkha'               : 'dz',
    'eastern cham'           : 'cjm',
    'egyptian arabic'        : 'arz',
    'egyptian'               : 'mjw',
    'elfdalian'              : 'ovd',
    'erzya'                  : 'myv',
    'eshtehardi'             : 'esh',
    'esperanto'              : 'eo',
    'estonian'               : 'et',
    'ewe'                    : 'ee',
    'faroese'                : 'fo',
    'fijian'                 : 'fj',
    'finnish'                : 'fi',
    'fon'                    : 'fon',
    'franco-provençal'       : 'frp',
    'french'                 : 'fr',
    'friulian'               : 'fur',
    'galician'               : 'gl',
    'gamilaraay'             : 'kld',
    'georgian'               : 'ka',
    'german low german'      : 'nds-de',
    'german'                 : 'de',
    'gilbertese'             : 'gil',
    'gooniyandi'             : 'gni',
    'greek'                  : 'el',
    'greek: (general)'       : 'el',
    'greenlandic'            : 'kl',
    'guaraní'                : 'gn',
    'gujarati'               : 'gu',
    'gulf arabic'            : 'afb',
    'hakka'                  : 'hak',
    'hausa'                  : 'ha',
    'hawaiian'               : 'haw',
    'hebrew'                 : 'he',
    'hijazi arabic'          : 'acw',
    'hiligaynon'             : 'hil',
    'hindi'                  : 'hi',
    'hopi'                   : 'hop',
    'hungarian'              : 'hu',
    'hunsrik'                : 'hrx',
    'iban'                   : 'iba',
    'icelandic'              : 'is',
    'ido'                    : 'io',
    'ilocano'                : 'ilo',
    'indonesian'             : 'id',
    'ingush'                 : 'inh',
    'interlingua'            : 'ia',
    'interlingue'            : 'ie',
    'iraqi arabic'           : 'acm',
    'irish'                  : 'ga',
    'italian'                : 'it',
    'japanese'               : 'ja',
    'javanese'               : 'jv',
    'jawi'                   : 'ms',
    'judeo-iraqi arabic'     : 'yhd',
    'kabardian'              : 'kbd',
    'kabyle'                 : 'kab',
    'kalmyk'                 : 'xal',
    'kambaata'               : 'ktb',
    'kannada'                : 'kn',
    'kapampangan'            : 'pam',
    'karachay-balkar'        : 'krc',
    'karakalpak'             : 'kaa',
    'kashubian'              : 'csb',
    'kazakh'                 : 'kk',
    'khakas'                 : 'kjh',
    'khasi'                  : 'kha',
    'khmer'                  : 'km',
    'kimaragang'             : 'kqr',
    'komi-zyrian'            : 'kpv',
    'korean'                 : 'ko',
    'kumyk'                  : 'kum',
    'kutenai'                : 'kut',
    'kyrgyz'                 : 'ky',
    'ladin'                  : 'lld',
    'lak'                    : 'lbe',
    'lao'                    : 'lo',
    'latgalian'              : 'ltg',
    'latin'                  : 'la',
    'latvian'                : 'lv',
    'laz'                    : 'lzz',
    'lebanese arabic'        : 'apc',
    'libyan'                 : 'ayl',
    'limburgish'             : 'li',
    'lithuanian'             : 'lt',
    'lower sorbian'          : 'dsb',
    'luxembourgish'          : 'lb',
    'lü'                     : 'khb',
    'macedonian'             : 'mk',
    'malagasy'               : 'mg',
    'malay'                  : 'ms',
    'malayalam'              : 'ml',
    'maltese'                : 'mt',
    'manchu'                 : 'mnc',
    'mandarin'               : 'cmn',
    'manx'                   : 'gv',
    'maori'                  : 'mi',
    'marathi'                : 'mr',
    'maricopa'               : 'mrc',
    'mazanderani'            : 'mzn',
    'mecayapan'              : 'nhx',
    'meänkieli'              : 'fit',
    'middle french'          : 'frm',
    'min dong'               : 'cdo',
    'min nan'                : 'nan',
    'mingrelian'             : 'xmf',
    'miyako'                 : 'mvi',
    'mongolian'              : 'mn',
    'montagnais'             : 'moe',
    'moroccan arabic'        : 'ary',
    'nama'                   : 'naq',
    'navajo'                 : 'nv',
    'nepali'                 : 'ne',
    'newar'                  : 'new',
    'ngazidja comorian'      : 'zdj',
    'nivkh'                  : 'niv',
    'nogai'                  : 'nog',
    'norman'                 : 'nrf',
    'north frisian'          : 'Mooring dialect',
    'northern khmer'         : 'kxm',
    'northern puebla'        : 'ncj',
    'northern sami'          : 'se',
    'northern thai'          : 'nod',
    'norwegian'              : 'no',
    'novial'                 : 'nov',
    'occitan'                : 'oc',
    'ojibwe'                 : 'oj',
    'okinawan'               : 'ryu',
    'old east slavic'        : 'orv',
    'old english'            : 'ang',
    'old french'             : 'fro',
    'old high german'        : 'goh',
    'old irish'              : 'sga',
    'oriya'                  : 'or',
    'oroqen'                 : 'orh',
    'ossetian'               : 'os',
    'ottoman turkish'        : 'ota',
    'pacoh'                  : 'pac',
    'panamint'               : 'par',
    'pashto'                 : 'ps',
    'persian'                : 'fa',
    'pipil'                  : 'ppl',
    'polish'                 : 'pl',
    'portuguese'             : 'pt',
    'punjabi'                : 'pa',
    'quechua'                : 'qu',
    'rohingya'               : 'rhg',
    'romagnol'               : 'rgn',
    'roman'                  : 'sh',
    'romani'                 : 'rom',
    'romanian'               : 'ro',
    'romansch'               : 'rm',
    'rumi'                   : 'ms',
    'russian'                : 'ru',
    'samoan'                 : 'sm',
    'sango'                  : 'sg',
    'sanskrit'               : 'sa',
    'sardinian'              : 'sc',
    'scottish gaelic'        : 'gd',
    'sebop'                  : 'sib',
    'semai'                  : 'sea',
    'seneca'                 : 'see',
    'seri'                   : 'sei',
    'shan'                   : 'shn',
    'shor'                   : 'cjs',
    'sichuan yi'             : 'ii',
    'sicilian'               : 'scn',
    'sindhi'                 : 'sd',
    'sinhalese'              : 'si',
    'slovak'                 : 'sk',
    'slovene'                : 'sl',
    'somali'                 : 'so',
    'sorani'                 : 'ku',
    'sotho'                  : 'st',
    'southern altai'         : 'alt',
    'southern sami'          : 'sma',
    'spanish'                : 'es',
    'sundanese'              : 'su',
    'swahili'                : 'sw',
    'swedish'                : 'sv',
    'sylheti'                : 'syl',
    'syriac'                 : 'arc',
    'tabasaran'              : 'tab',
    'tagal murut'            : 'mvv',
    'tagalog'                : 'tl',
    'tahitian'               : 'ty',
    'tajik'                  : 'tg',
    'tamil'                  : 'ta',
    'taos'                   : 'twf',
    'tatar'                  : 'tt',
    'telugu'                 : 'te',
    'tetum'                  : 'tet',
    'thai'                   : 'th',
    'tibetan'                : 'bo',
    'tigre'                  : 'tig',
    'tigrinya'               : 'ti',
    'tongan'                 : 'to',
    'torres strait creole'   : 'tcs',
    'translingual'           : 'mul',
    'tswana'                 : 'tn',
    'turkish'                : 'tr',
    'turkmen'                : 'tk',
    'tutong'                 : 'ttg',
    'tuvan'                  : 'tyv',
    'uab meto'               : 'aoz',
    'udmurt'                 : 'udm',
    'ukrainian'              : 'uk',
    'umbundu'                : 'umb',
    'unami'                  : 'unm',
    'upper sorbian'          : 'hsb',
    'urdu'                   : 'ur',
    'uyghur'                 : 'ug',
    'uzbek'                  : 'uz',
    'vietnamese'             : 'vi',
    'volapük'                : 'vo',
    'walloon'                : 'wa',
    'waray-waray'            : 'war',
    'welsh'                  : 'cy',
    'west coast bajau'       : 'bdr',
    'west frisian'           : 'fy',
    'western apache'         : 'apw',
    'westrobothnian'         : 'gmq-bot',
    'white hmong'            : 'mww',
    'wik-mungkan'            : 'wim',
    'wolof'                  : 'wo',
    'wu'                     : 'wuu',
    'xhosa'                  : 'xh',
    'yaeyama'                : 'rys',
    'yakkha'                 : 'ybh',
    'yakut'                  : 'sah',
    'yiddish'                : 'yi',
    'yindjibarndi'           : 'yij',
    'yoron'                  : 'yox',
    'yoruba'                 : 'yo',
    'zazaki'                 : 'zza',
    'zhuang'                 : 'za',
    'zulu'                   : 'zu',
    "ge'ez"                  : 'gez',
    "k'iche'"                : 'quc',
    "mi'kmaq"                : 'mic',
    "tz'utujil"              : 'tzj',
}


def trans_see( t ):
    yield t.arg(0)


def t( t ):
    yield t.arg(1)


def t_plus( t ):
    yield t.arg(1)


def trans_top( t ):
    yield t.arg(0)


def qualifier( t ):
    yield t.arg(0)


def t_egy( t ):
    yield t.arg('h')


def syn( t ):
    for a in itertools.islice( t.positional_args(), 1, None ):
        yield a.get_text()


def sense( t ):
    yield t.arg(0)


def gloss( t ):
    yield t.arg(0)


def stub( t ):
    yield from ()



TEMPLATES = {
    'trans-see' : trans_see,    # {{trans-see|cat|cat/translations#Noun}}
    't'         : t,            # {{t|de|Pantoffeltiger|m}},
    't+'        : t_plus,       # {{t+|fr|chat|m}}, {{t+|fr|chatte|f}}
    't-egy'     : t_egy,        # {{t-egy|mjw|h=mi-i-w-E13}}
    'trans-top' : trans_top,    # {{trans-top|domestic species}} ... {{trans-bottom}}
    'q'         : qualifier,    # {{q|cat(s)}}, {{q|a single cat}}, {{q|several cats}}
    'qualifier' : qualifier,
    'i'         : qualifier,
    'qual'      : qualifier,
    'syn'       : syn,          # * {{syn|en|powerful|Thesaurus:strong}}
    'synonyms'  : syn,          #
    'synonym of': syn,          #
    'sense'     : sense,        # * {{sense|an oath or affirmation}} [[promise]], [[vow]], [[word]] {{qualifier|informal}}
    'gloss'     : gloss,        # * [[eye]] {{gloss|organ of vision}}
}



# {{...}} -> [words]
#
# example:
# {{synonym of|en|job center}} -> ['job center']
# to words()

def to_words( t ):
    try:
        yield from TEMPLATES[ t.name ]( t )

    except KeyError:
        yield from ()
