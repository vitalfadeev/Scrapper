import unittest


test_file = 'wiktionary.tests.test_scrap'
suites = [
    unittest.defaultTestLoader.loadTestsFromName( test_file )
]
test_suite = unittest.TestSuite( suites )
test_runner = unittest.TextTestRunner().run( test_suite )
