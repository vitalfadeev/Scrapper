import functools
import logging
import math
import sqlite3

from Scrapper_DB import DBWrite, DBRead, DBExecute
from _dev_scripts.Scrapper_Item import Str
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
        return []

    wids = ",".join( wikidata_id_list )

    rows =  DBRead(
        DBWikidata,
        sql="SELECT LabelName FROM wikidata WHERE CodeInWiki IN (?)",
        params=[wids] )

    if rows:
        return ",".join( row[0] for row in rows )
    else:
        log.warning( "No record for %s", wids )
        return []


def get_sentences_with_label( Description, LabelName ):
    return []


@functools.lru_cache( maxsize=32 )
def wds_value_of( s: str ):
    rows = DBRead( DBWikidata, sql="SELECT * FROM wikidata WHERE PrimaryKey=?", params=[s], cls=WordItem )
    #rows = Read( "SELECT * FROM wikidata WHERE PrimaryKey=?", 'CAT-FELIDAE' ).as_objects( WordItem )
    try:
        wd = next( rows )

    except StopIteration:
        return None

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
        math.sqrt( len( wd.ExplainationExamplesTxt ) ) + \
        math.sqrt( len( wd.ExplainationTxt ) )

    return 1


def merge_words( w, wd, ):
    w.PK                = wd.PrimaryKey
    w.SelfUrlWikidata   = wd.SelfUrl
    w.LabelName         = wd.LabelName
    w.LanguageCode      = wd.LanguageCode
    w.Description       = wd.Description
    w.AlsoKnownAs       = to_names( wd.AlsoKnownAs )
    # wd.WikipediaENURL
    # wd.WikipediaFRURL
    # wd.WikipediaDEURL
    # wd.WikipediaITURL
    # wd.WikipediaESURL
    # wd.WikipediaRUURL
    # wd.WikipediaPTURL
    w.Ext_Wikipedia_URL += [getattr( wd, "Wikipedia{}URL".format( wd.LanguageCode.upper() ) )]
    # wd.EncyclopediaBritannicaEN
    # wd.EncyclopediaUniversalisFR
    # wd.DescriptionUrl
    w.Hypernymy         += to_names( wd.Instance_of )
    w.Hypernymy         += to_names( wd.Subclass_of )
    w.Meronymy          += to_names( wd.Part_of )
    w.Translation_EN    += wd.Translation_EN
    w.Translation_FR    += wd.Translation_FR
    w.Translation_DE    += wd.Translation_DE
    w.Translation_IT    += wd.Translation_IT
    w.Translation_ES    += wd.Translation_ES
    w.Translation_RU    += wd.Translation_RU
    w.Translation_PT    += wd.Translation_PT
    w.CountTotalOfWikipediaUrl = wd.WikipediaLinkCountTotal
    # wd.EncyclopediaGreatRussianRU

    w.FromWD.append( wd.PrimaryKey )


def convert_wikidata_to_word( wd: WikidataItem ) -> WordItem:
    log.info( wd )

    w = WordItem()

    # merge
    merge_words( w, wd )

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

    wds = wds_value_of( 'CAT-FELIDAE' )

    if wds is None:
        return w

    #
    x = wds / wds / 2

    if x <= 0:
        w.LabelNamePreference = 0
    else:
        w.LabelNamePreference = 1

    return w


def load_wikidata_one( lang, label ):
    with sqlite3.connect( "wikidata.db", timeout=5.0 ) as DBWWikidata:
        with sqlite3.connect( "word.db", timeout=5.0 ) as DBWord:

            for wd in DBRead( DBWWikidata, table="wikidata", cls=WikidataItem, where="LanguageCode=? COLLATE NOCASE AND LabelName=? COLLATE NOCASE", params=[ lang, label ] ):
                log.info( "%s", wd )

                w = convert_wikidata_to_word( wd )
                DBWrite( DBWord, w, table="words", if_exists="fail" )

                DBExecute( DBWWikidata, "UPDATE wikidata SET Operation_Merging = 1 WHERE PrimaryKey = ?", wd.PrimaryKey )


def load_wikidata():
    with sqlite3.connect( "wikidata.db", timeout=5.0 ) as DBWWikidata:
        with sqlite3.connect( "word.db", timeout=5.0 ) as DBWord:

            for wd in DBRead( DBWWikidata, table="wikidata", cls=WikidataItem ):
                log.info( "%s", wd )

                w = convert_wikidata_to_word( wd )
                DBWrite( DBWord, w, table="words", if_exists="fail" )

                DBExecute( DBWWikidata, "UPDATE wikidata SET Operation_Merging = 1 WHERE PrimaryKey = ?", wd.PrimaryKey )

