import multiprocessing
import itertools
import multiprocessing.dummy
import threading
import queue

workers = 2
lang = "en"
reader = range(10)


def scrap_one( lang, page ):
    print( "f", (lang, page) )
    #return [lang, page]

def scrap_one_wrapper( args ):
    scrap_one( *args )


q = queue.Queue()

for page in reader:
    t = threading.Thread(target=scrap_one, args = (q, page))
    t.daemon = True
    t.start()

s = q.get()
print( s )

