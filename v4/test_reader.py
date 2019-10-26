from v4.reader import Read


if __name__ == "__main__":
    for item in Read( "cached/dewiki-latest-pages-articles.xml.bz2" ):
        print( item )
        break

    for item in Read( "cached/dewiki-latest-pages-articles.xml.bz2" ).head( 3 ):
        print( item )

    for item in Read( "cached/dewiki-latest-pages-articles.xml.bz2" )[:3]:
        print( item )

    for item in Read( "cached/dewiki-latest-pages-articles.xml.bz2" )[3]:
        print( item )

    for item in Read( "cached/dewiki-latest-pages-articles.xml.bz2" ).by_element( 'page' ):
        print( item )
        break

    for item in Read( "v4/tests/plain.txt" ).by_line().head( 3 ):
        print( item )

    for item in Read( "v4/tests/plain.txt" ).by_line()[:3]:
        print( item )

    for item in Read( "v4/tests/plain.txt" ).by_line()[2]:
        print( item )


# stream
# range
#   as pandas:
#     .select()
#     .head()
#     .where( row['time'] == 'Dinner' and row['tip'] > 5 )
#     .groupby()
#     .count()
#     .tail()
#     .sort()
#   as jQuery:
#     .each()
#   as DLang:
#     .by_line()
#     .by_pairs()
#   with XML:
#     .by_element()
#     .by_tag()
# pandas can use it
#   not pandas, because pandas not stream-able. how to parse 37 GB wikidata.json.dump ?

# converters
#   Wikipedia
#   Wiktionary
#   Wikidata
#   VerbConjugations

# to row

# row save to
#   db sqlite/mysql
#   db json
#   db txt
#   db xml
