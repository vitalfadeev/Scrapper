import unittest
from conjugator.Scrapper_Conjugator import  check_connection, get_conjugations


class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass


    def test_1_check_coonnection(self):
        check_connection()


    def test_2_get_conjugations(self):
        lang = 'eng'
        verb = 'do'
        words = get_conjugations( lang, verb )
        for word in words:
            print( word )
        print( len(words) )
        self.assertIsInstance( words, list )
        self.assertEqual( len(words), 66 )

