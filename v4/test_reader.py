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


