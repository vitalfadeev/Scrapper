import os
import itertools
from wiktionary.Scrapper_Wiktionary import Dump, filterPageProblems
from wiktionary.Scrapper_Wiktionary_WikitextParser import Section, Header, Template, Li, Link, String, Container
from Scrapper_Helpers import save_to_json


sense_templates = {}
lang = 'en'

os.chdir( '..' )

reader = filter( filterPageProblems, Dump( lang ).download().getReader() )
for i, page in enumerate( reader ):
    lexems = page.to_lexems()

    for lexem in lexems:
        if isinstance( lexem, Container ):
            for l in itertools.chain( [lexem], lexem.find_all( recursive=True ) ):
                if isinstance( l, Template ):
                    t = l
                    if t.name == 'sense':
                        print( t )
                        for c in t.find_objects( Template, recursive=True ):
                            print( "  ", c )
                            sense_templates[ c.name ] = 1

    # save over each 1000
    if i % 100 == 0:
        save_to_json( sense_templates, 'sense_templates.json' )

save_to_json( sense_templates, 'sense_templates.json' )
