#from wiktionary import Scrapper_Wiktionary
#Scrapper_Wiktionary.scrap( workers=1 )

import os
import unittest

os.chdir('wiktionary')
os.chdir('tests')


testmodules = [
    'wiktionary.tests.test_scrap',
]

suite = unittest.TestSuite()

for t in testmodules:
    try:
        # If the module defines a suite() function, call it to get the suite.
        mod = __import__(t, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
    except (ImportError, AttributeError):
        # else, just load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner().run(suite)
