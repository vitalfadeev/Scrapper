import os
import itertools
import collections
from wiktionary.Scrapper_Wiktionary import Dump, filterPageProblems
from wiktionary.Scrapper_Wiktionary_WikitextParser import Section, Header, Template, Li, Link, String, Container
from Scrapper_Helpers import save_to_json


root = collections.defaultdict( dict )
section = None
lang = 'en'

os.chdir( '..' )

def scan_recursive( root, lexems ):
    section = root

    for lexem in lexems:
        if isinstance( lexem, Container ):
            #
            if isinstance( lexem, Header ):
                if lexem.name in root:
                    section = root[ lexem.name ]
                else:
                    section = { }
                    root[ lexem.name ] = section

                continue

            #
            subtree = {}
            scan_recursive( subtree, lexem.childs )

            #
            k = lexem.name
            if not k:
                k = type( lexem ).__name__

            if isinstance( lexem, Template ):
                k = '{{' + lexem.name + '}}'

            if isinstance( lexem, Li ):
                k = lexem.base

            #
            if isinstance( lexem, String ):
                continue

            #
            if k in section:
                section[ k ].update( subtree )
            else:
                section[ k ] = subtree


reader = filter( filterPageProblems, Dump( lang ).download().getReader() )
for i, page in enumerate( reader ):
    lexems = page.to_lexems()
    section = None

    scan_recursive( root, lexems )

    # save over each 1000
    if i % 1000 == 0:
        save_to_json( root, 'section_templates.json' )

save_to_json( root, 'section_templates.json' )

