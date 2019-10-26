from v4.reader import Read

if __name__ == "__main__":
    f = Reader( "cached/dewiki-latest-pages-articles.xml.bz2" )
    #block = f.read( 10 )
    #print( block )
    for action, elem in f:
        print( action, elem )
        break
