import mputil
import itertools
import time


def scrap_one( lang, page ):
    print( "f", (lang, page) )
    time.sleep( 3 )
    return [lang, page]

def scrap_one_wrapper( args ):
    return scrap_one( *args )


def get_reader():
    for x in range( 10 ):
        print( "readed: ", x )
        yield x


if __name__ == '__main__':
    lang = "en"

    result = mputil.lazy_imap(
        data_processor=scrap_one_wrapper,
        data_generator=zip( itertools.repeat( lang ), get_reader() ),
        n_cpus=3
    )

    for item in result:
        print( item )



if 0:
    import itertools
    from multiprocessing import Pool
    from time import sleep


    def scrap_one( lang, page ):
        print( "f", (lang, page) )
        sleep( 3 )
        return [lang, page]

    def scrap_one_wrapper( args ):
        return scrap_one( *args )


    def get_reader():
        for x in range( 10 ):
            print( "readed: ", x )
            yield x


    if __name__ == '__main__':
        lang = "en"
        p = Pool( processes=2 )

        data = p.imap_unordered( scrap_one_wrapper, zip( itertools.repeat( lang ), get_reader() ), chunksize=1 )

        p.close()
        p.join()
        print(data)


if 0:
    import multiprocessing as mp

    def foo(q):
        q.put('hello')
        return 1

    if __name__ == '__main__':
        mp.set_start_method('spawn')
        q = mp.Queue()
        p = mp.Process(target=foo, args=(q,))
        p.start()
        print( 2, q.get() )
        p.join()



if 0:
    import itertools
    from multiprocessing.dummy import Pool as ThreadPool

    workers = 2
    lang = "en"
    reader = range(10)


    def scrap_one( lang, page ):
        print( "f", (lang, page) )
        return [lang, page]

    def scrap_one_wrapper( args ):
        scrap_one( *args )


    pool = ThreadPool(4)
    results = pool.map( scrap_one_wrapper, zip( itertools.repeat( lang ), reader ) )

    print( results )

