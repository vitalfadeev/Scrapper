from timeit import timeit
import sys
print("Python", sys.version)

MILLION_NUMBERS = list( range(1000000) )

# simple
print( "simple:" )
def f1():
    output = []
    for x in MILLION_NUMBERS:
        output.append( x )

    return output

def f2():
    return list( filter( None, MILLION_NUMBERS ) )

def f3():
    return [ x for x in MILLION_NUMBERS]

print( timeit(stmt=f1, number=100) )
print( timeit(stmt=f2, number=100) )
print( timeit(stmt=f3, number=100) )

# w/condition
print( "w/condition:" )
def f4():
    output = []
    for x in MILLION_NUMBERS:
        if x % 2 == 0:
            output.append( x )

    return output

def f5():
    return list( filter( lambda x: x % 2 == 0, MILLION_NUMBERS ) )

def f6():
    return [ x for x in MILLION_NUMBERS if x % 2 == 0 ]

print( timeit(stmt=f4, number=100) )
print( timeit(stmt=f5, number=100) )
print( timeit(stmt=f6, number=100) )
