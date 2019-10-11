import unittest
from wiktionary.Scrapper_Wiktionary_Conjugations import  check_connection, get_conjugations, VERBIX_URL


class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass


    def test_1_check_coonnection(self):
        check_connection()


    def test_2_get_conjugations(self):
        lang = 'eng'
        verb = 'do'
        words = get_conjugations( lang, verb )
        print( words )

