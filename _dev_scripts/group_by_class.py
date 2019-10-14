import itertools


class Li:
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return "Li(" + self.s + ")"


class Dl:
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return "Li(" + self.s + ")"


def find_chains( lexems: list ):
    # lexems
    # - (li, lexem)
    # - (tx, lexem)
    # - (li, lexem)
    # - (tx, lexem)

    iterator = iter( lexems )

    for lexem in iterator:
        if isinstance( lexem, Li ):
            yield ( 'li', lexem )
        else:
            yield ( 'tx', lexem )


def group( lexems: list ):
    # chains:
    # - (li, lexem)
    # - (li, lexem)
    # - (li, lexem)
    # - (tx, lexem)
    # to groups:
    # - (li, (lexem, lexem, lexem)
    # - (tx, (lexem)
    chains = find_chains( lexems )
    groups = itertools.groupby( chains, lambda x: x[ 0 ] )
    return groups


lexems = [
    Li('1.1'),
    Li('1.2'),
    Li('1.3'),
    'str-1.1',
    'str-1.2',
    'str-1.3',
    Li( '2.1.' ),
    'str-2.1',
]

def keyfn( x ):
    if isinstance( x, Li ):
        return 'li'
    elif isinstance( x, Dl ):
        return 'dl'
    else:
        return 'tx'

grouped = itertools.groupby( lexems, keyfn )

for k, x in grouped:
    print( k, list(x) )
