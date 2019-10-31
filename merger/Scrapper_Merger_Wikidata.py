import functools
import logging
import math
import sqlite3

from Scrapper_Item import Str, ItemProxy
from _dev_scripts.v4.range import R
from _dev_scripts.v4.reader import read
from merger.Scrapper_Merger_Item import WordItem
from wikidata.Scrapper_Wikidata import DBWikidata
from wikidata.Scrapper_Wikidata_Item import WikidataItem

log    = logging.getLogger(__name__)


def LabelType( wd: WikidataItem ) -> str:
    # From Description keep 3 first words having a lenght>=4
    # and starting with letter,
    # then do InitalUpperCase
    # and concatenate with minus sign
    # (example "capital city of Portugal" = "Capital-City-Portugal")

    from _dev_scripts.v4.range import Range

    LabelTypeWD = Range( wd.Description ) \
        .get_words() \
        .map( str.strip )  \
        .filter( lambda s: len(s) > 0 ) \
        .filter( lambda s: len(s) < 4 ) \
        .filter( lambda s: s[0].isalpha() ) \
        .map( Str.InitalUpperCase ) \
        .join( '-' )

    return LabelTypeWD


def to_names( wikidata_id_list ):
    if wikidata_id_list is None:
        return None

    def to_name( wid ):
        return R( DBWikidata ) \
            .from_sql( "SELECT * FROM wikidata WHERE CodeInWiki = ?", wid, cls=WikidataItem ) \
            .first() \
            .LabelName

    return R( wikidata_id_list ).map( to_name ).as_list()


def get_sentences_with_label( Description, LabelName ):
    return []


@functools.lru_cache( maxsize=32 )
def wds_value_of( wid ):
    return 0


def convert_wikidata_to_word( wd: WikidataItem ) -> WordItem:
    log.info( wd )

    w = WordItem()

    w.PK                       = wd.PrimaryKey
    w.LabelName                = wd.LabelName
    w.LabelType                = LabelType( wd )
    w.LanguageCode             = wd.LanguageCode
    w.Description              = wd.Description
    w.AlsoKnownAs              = wd.AlsoKnownAs
    w.SelfUrlWikidata          = wd.SelfUrl
    w.Instance_of              = to_names( wd.Subclass_of )
    w.Subclass_of              = to_names( wd.Instance_of )
    w.Part_of                  = to_names( wd.Part_of )
    w.Translation_EN           = wd.Translation_EN
    w.Translation_FR           = wd.Translation_FR
    w.Translation_DE           = wd.Translation_DE
    w.Translation_IT           = wd.Translation_IT
    w.Translation_ES           = wd.Translation_ES
    w.Translation_RU           = wd.Translation_RU
    w.Translation_PT           = wd.Translation_PT
    w.Ext_Wikipedia_URL        = getattr( wd, "Wikipedia{}URL".format( wd.LanguageCode.upper() ) )
    w.CountTotalOfWikipediaUrl = wd.WikipediaLinkCountTotal

    # PKN preparing
    # LabelNamePreference
    ExplainationExamplesTxt = get_sentences_with_label( wd.Description, wd.LabelName )
    ExplainationTxt = wd.Description

    wds = \
        len( wd.AlsoKnownAs ) + \
        len( wd.Instance_of ) + \
        len( wd.Subclass_of ) + \
        len( wd.Part_of ) + \
        len( wd.Translation_EN ) + \
        len( wd.Translation_PT ) + \
        len( wd.Translation_DE ) + \
        len( wd.Translation_ES ) + \
        len( wd.Translation_FR ) + \
        len( wd.Translation_IT ) + \
        len( wd.Translation_RU ) + \
        math.sqrt( wd.WikipediaLinkCountTotal ) + \
        math.sqrt( len( ExplainationExamplesTxt ) ) + \
        math.sqrt( len( ExplainationTxt ) )

    # then divide by value of ( CAT-FELIDAE ) and divide by 2
    # If <0 then : =0 elif >1 then : =1

    x = wds / wds_value_of( 'CAT-FELIDAE' ) / 2

    if x <= 0:
        w.LabelNamePreference = 0
    else:
        w.LabelNamePreference = 1

    return w


def load_wikidata():
    with sqlite3.connect( "wikidata.db", timeout=5.0 ) as DBWWikidata:
        with sqlite3.connect( "word.db", timeout=5.0 ) as DBWord:

            read( DBWWikidata, table="wikidata", cls=WikidataItem ) \
                .map( convert_wikidata_to_word ) \
                .write( DBWord, table="words", if_exists="fail" )


