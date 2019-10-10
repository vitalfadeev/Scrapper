import os
import unittest
from wiktionary import Scrapper_Wiktionary_RemoteAPI


class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass


    def test_1_parse(self):
        title = 'cat'
        text = "# An animal of the family [[Felidae]]:"
        expected = '<div class="mw-parser-output"><ol><li>An animal of the family <a href="/wiki/Felidae" title="Felidae">Felidae</a>:</li></ol></div>'

        parsed_text = Scrapper_Wiktionary_RemoteAPI.parse( title, text )

        self.assertEqual( parsed_text, expected )


    def test_2_expand_templates(self):
        title = 'cat'
        templates = [
            "# An animal of the family [[Felidae]]:",
            "#* {{quote-book|en|year=2011|author=Karl Kruszelnicki|title=Brain Food|isbn=1466828129|page=53|passage=Mammals need two genes to make the taste receptor for sugar. Studies in various '''cats''' (tigers, cheetahs and domestic cats) showed that one of these genes has mutated and no longer works.}}",
            "#: {{syn|en|felid}}",
        ]
        expected = [
            "# An animal of the family Felidae:",
            "#* 2011,  Karl Kruszelnicki,  Brain Food, →ISBN, page 53:Mammals need two genes to make the taste receptor for sugar. Studies in various cats (tigers, cheetahs and domestic cats) showed that one of these genes has mutated and no longer works.",
            "#: Synonym: felid",
        ]
        converted = Scrapper_Wiktionary_RemoteAPI.expand_templates( title, templates )
        self.assertListEqual( converted, expected )


    def test_3_get_wikitext(self):
        title = 'cat'
        text = Scrapper_Wiktionary_RemoteAPI.get_wikitext( title )
        self.assertIsInstance( text, str )
        self.assertRegex( text, '==English==' )
        self.assertRegex( text, '===Noun===' )


    def test_4_get_wikitext_2(self):
        title = 'cat/translations'
        text = Scrapper_Wiktionary_RemoteAPI.get_wikitext( title )
        self.assertIsInstance( text, str )
        self.assertRegex( text, '==English==' )
        self.assertRegex( text, '===Noun===' )
        self.assertRegex( text, '====Translations====' )


if __name__ == '__main__':
    unittest.main()

