from .reader import Reader
from .writer import Writer
from .converter import Converter


def main():
    # reader = Reader( "dump.xml.bz2" )
    # writer = Writer( "sqlite:///scrapped.db" )
    # converter = wikipedia.Converter()
    # converter = wiktionary.Converter()
    # converter = conjugator.Converter()
    converter = Converter()

    with Reader( "dump.xml.bz2" ) as reader:
        with Writer( "sqlite:///scrapped.sqlite3" ) as writer:
            for item in converter.convert( reader ):
                writer.write( item )


if __name__ == "__main__":
    main()

# reader = Reader( "dump.xml.bz2" )
# here will be chain of reader: file -> bz2 -> xml ->

# read DB
# with Reader( "sqlite:///scrapped.sqlite3" ) as reader:
#   for item in reader:
#      print( item )
#
# with Reader( "wiktionary.item" ) as reader:
#   for item in reader:
#      print( item )
#

# with Reader( "sqlite:///scrapped.sqlite3" ) as db_reader:
#   with ItemReader( db_reader, WiktionaryItem ) as reader:
#     for item in reader:
#       print( item )
#

# with Reader( "sqlite:///scrapped.sqlite3" ) as db_reader:
#   with Reader( db_reader, "SELECT * FROM wiktionary WHERE lang = 'en'" ) as reader:
#     for item in reader:
#       print( item )
#

# Reader( "dump.xml.bz2" )
#   open( "dump.xml.bz2" )
#     bz2.open( f )
#       xml.open( f )

# Reader( "http://www/dump.xml.bz2" )
#   requests.get( "http://www/dump.xml.bz2" )
#   open( "dump.xml.bz2" )
#     bz2.open( f )
#       xml.open( f )

# Reader( "http://www/page.html" )
#   requests.get( "http://www/page.html" )
#   open( "page.html" )
#     html.open( f )

# Reader( "http://www/rss.xml" )
#   requests.get( "http://www/rss.xml" )
#   open( "rss.xml" )
#     xml.open( f )
