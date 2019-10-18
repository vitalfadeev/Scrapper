from wiktionary import Scrapper_Wiktionary
Scrapper_Wiktionary.scrap( workers=1 )
exit(7)

import unittest


test_file = 'wiktionary.tests.test_scrap'
suites = [
    unittest.defaultTestLoader.loadTestsFromName( test_file )
]
test_suite = unittest.TestSuite( suites )
test_runner = unittest.TextTestRunner().run( test_suite )