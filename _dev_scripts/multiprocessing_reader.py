import itertools
from multiprocessing import Pool
from time import sleep


def f( x ):
    print( "f()" )
    sleep( 3 )
    return x


def get_reader():
    for x in range( 10 ):
        print( "readed: ", x )
        value = " " * 1024 * 64 # 64k
        yield value


if __name__ == '__main__':
    p = Pool( processes=2 )

    data = p.imap( f, get_reader() )

    p.close()
    p.join()

# python -m memory_profiler multiprocessing_reader.py
# mprof run --include-children python multiprocessing_reader.py
# mprof plot --output memory-profile.png
