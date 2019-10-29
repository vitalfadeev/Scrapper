import re

from Scrapper_Item import Str, ItemProxy
from wikidata.Scrapper_Wikidata_Item import WikidataItem


def LabelTypeWD( wd: WikidataItem ):
    # From Description keep 3 first words having a lenght>=4
    # and starting with letter,
    # then do InitalUpperCase
    # and concatenate with minus sign
    # (example "capital city of Portugal" = "Capital-City-Portugal")

    wd = ItemProxy( wd )

    LabelTypeWD = wd.Description.get_words() \
        .map( str.strip ) \
        .filter( lambda s: len(s) > 0 ) \
        .filter( lambda s: len(s) < 4 ) \
        .filter( lambda s: s[0].isalpha() ) \
        .map( Str.InitalUpperCase ) \
        .join( '-' )

    return LabelTypeWD


def Instance_of( wd: WikidataItem ):
    lst = wd.Instance_of.map(
        lambda wid:
            WDDB.select( wd.CodeInWiki == wid ).first().LabelName
    )
    return lst


def Subclass_of( wd: WikidataItem ):
    lst = wd.Subclass_of.map(
        lambda wid:
            WDDB.select( wd.CodeInWiki == wid ).first().LabelName
    )
    return lst


def Part_of( wd: WikidataItem ):
    lst = wd.Part_of.map(
        lambda wid:
            WDDB.select( wd.CodeInWiki == wid ).first().LabelName
    )
    return lst


def Ext_Wikipedia_URL( wd: WikidataItem ):
    # wikipedia for the word of current LanguageCode
    return getattr( wd, "wd.Wikipedia{}URL".format(wd.LanguageCode.upper()) )


def CountTotalOfWikipediaUrl( wd: WikidataItem ):
    # (total count of wikipedia links languages in wikidata : 0..250)
    return wd.WikipediaLinkCountTotal
