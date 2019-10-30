import re

from Scrapper_Item import Str, ItemProxy
from _dev_scripts.v4.range import R
from wikidata.Scrapper_Wikidata import DBWWikidata
from wikidata.Scrapper_Wikidata_Item import WikidataItem


def LabelType( wd: WikidataItem ):
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
        return R( DBWWikidata ) \
            .from_sql( "SELECT * FROM wikidata WHERE CodeInWiki = ?", wid, cls=WikidataItem ) \
            .first() \
            .LabelName

    return R( wikidata_id_list ).map( to_name ).as_list()


def Instance_of( wd: WikidataItem ):
    return to_names( wd.Subclass_of )


def Subclass_of( wd: WikidataItem ):
    return to_names( wd.Instance_of )


def Part_of( wd: WikidataItem ):
    return to_names( wd.Part_of )


def Ext_Wikipedia_URL( wd: WikidataItem ):
    # wikipedia for the word of current LanguageCode
    return getattr( wd, "Wikipedia{}URL".format(wd.LanguageCode.upper()) )


def CountTotalOfWikipediaUrl( wd: WikidataItem ):
    # (total count of wikipedia links languages in wikidata : 0..250)
    return wd.WikipediaLinkCountTotal
