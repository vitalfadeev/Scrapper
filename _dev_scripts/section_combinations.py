import os
import itertools
import collections
from wiktionary.Scrapper_Wiktionary import Dump, filterPageProblems
from Scrapper_Helpers import save_to_json

lang = 'en'
os.chdir( '..' )


def dict_merge( dct: dict, merge_dct: dict ):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.items():
        if (k in dct and isinstance( dct[ k ], dict )
                and isinstance( merge_dct[ k ], collections.Mapping )):
            dict_merge( dct[ k ], merge_dct[ k ] )
        else:
            dct[ k ] = merge_dct[ k ]



# tree
class Node(list):
    def __init__(self):
        super().__init__()
        self.root = None
        self.level = 0
        self.title = ''
        self.parent = None

    def append( self, child ):
        child.parent = self
        super().append( child )

    def to_dict( self ) -> dict:
        d = {}

        for c in self:
            d[c.title] = c.to_dict()

        return d


bigtree = {}

reader = filter( filterPageProblems, Dump( lang ).download().getReader() )

for i, page in enumerate( reader ):
    # 1. make tree
    # 2. merge in big tree
    # 3. save

    #
    root = Node()
    last = root

    # 1. make tree
    for line in page.text.splitlines():
        # find header
        if line.startswith('='):
            # level
            level = sum( 1 for _ in itertools.takewhile( lambda x: x == '=', line ) )
            node = Node()
            node.level = level
            node.title = line

            # find parent
            if last.level < node.level:
                last.append( node )
                last = node

            elif last.level == node.level:
                last.parent.append( node )
                last = node

            elif last.level > node.level:
                # find parent
                parent = last

                while parent is not root:
                    if parent.level < node.level:
                        break  # found
                    else:
                        parent = parent.parent

                parent.append( node )
                last = node

    # 2. merge in big tree
    dict_merge( bigtree, root.to_dict() )

    # 3. save over each 1000
    if i % 1000 == 0:
        save_to_json( bigtree, 'section_combinations.json' )

# 4. save result
save_to_json( bigtree, 'section_combinations.json' )

