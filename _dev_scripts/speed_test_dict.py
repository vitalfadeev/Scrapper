from timeit import timeit
import sys
print("Python", sys.version)

d = { "one":1, "two":2, "three":3 }

# simple
def f1():
    if "one" in d:
        x = d["one"]

def f2():
    try:
        x = d["one"]
    except KeyError:
        pass


def f3():
    try:
        x = d["none"]
    except KeyError:
        pass

def f4():
    x = d.get("none", None)



print( timeit(stmt=f1, number=10000000) )
print( timeit(stmt=f2, number=10000000) )
print( timeit(stmt=f3, number=10000000) )
print( timeit(stmt=f4, number=10000000) )
