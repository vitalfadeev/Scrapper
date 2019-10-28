from _dev_scripts.v4.reader import Read, read


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

    for item in Read( "v4/wikipedia.sqlite3" )[:3]:
        print( item )
        
    #
	lang = "en"
    url = "https://dumps.wikimedia.org/" + lang + "wiki/latest/" + lang + "wiki-latest-pages-articles.xml.bz2"

    read( url, caching=True ).filter().convert( converter, workers=1 ).filter().write( "v4/wikipedia.sqlite3" )
    # download to cache, and parse while downloading: parse downloaded strem
    # save state: savepoint
    # on restart:
    #   case 1: Resume downloading. Continue parsing fron savepoint
    #   case 2: Resume downloading. Parse fron start
    #   case 3: Resume downloading. Parse one item
    #   case 4: Parse one item

    # mpdule WiktionaryConverter
    def converter( row ):
        xml = row

        # parse
        wikitext = xml.by_element( "page" ).text  	# by_element( "page" )

        lexems = wikoo.parse( wikitext )  			# convert( 'wiki' )

        toc = build_toc_tree( lexems )    			# convert( 'wikioo_toc' )

        page = Page( lang, row, wikitext, lexems, toc )

        # parents = {
        #   "/"   : { "lang": "en" },
        #   "bz2" : {},
        #   "xml" : { "page": page },
        #   "."   : { "toc": toc },
        # }

		# analyze
		# page
		#   sections
		#     sences
		#       words | links

        # like a DOM
        # Node
        #   Node
        #     Node
        #       Node atts

        # Build true structure

        # Lang:
        #   Etymology:
        #       Part-of-speech:
        #           explanation
        #           Synonyms:
        #               sense:
        #                   word1, word2
        #       Synonyms:
        # Synonyms:
        #

        # 1. find lang
        # 2. under lang find Etymology
        # 3. under each Etymology find Part-of-speech
        # 4. under each Part-of-speech find explanation
        # 5. under lang, each Etymology, each Part-of-speech find Synonyms
        # 6. under lang, each Etymology, each Part-of-speech find *yms
        # 7. under lang, each Etymology, each Part-of-speech find Translations
        # 8. under lang, each Etymology, each Part-of-speech find SeeAlso
        # 9. under lang, each Etymology, each Part-of-speech find Related

        # - find each section Synonyms
        # - detect nearest parent Section: lang, Etymology, each Part-of-speech


        # 1. parse raw -> lexems
        # 2. build tree -> sections
        # 3. find Synonyms -> { "Synonyms": { parents: [Noun, Étymologie, Français] } }
        #

        items = []

        return items
		


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
