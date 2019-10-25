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

