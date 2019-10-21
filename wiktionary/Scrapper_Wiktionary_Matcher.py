"""
PKS Matcher helper

It return matched sentence for given `explanation_sense_txt`.
"""

import Scrapper_IxiooAPI

class Matcher:
    @classmethod
    def match( cls, explanation_sense_txt, explanation_senses, section_senses ):
        """
        It return matched sentence for given `explanation_sense_txt`.

        Args:
            explanation_sense_txt (str):    Explanations string
            explanation_senses (list        All explanation sentences
            section_senses (list):          All Translation (or synonyms/hyponums/...) sentences

        Returns:
            (str)   Matched sentence.

        """
        if section_senses and explanation_sense_txt:
            # list conerted to tuples for hashing for use with `lru_cache`
            matches = Scrapper_IxiooAPI.Match_List_PKS_With_Lists_Of_PKS( tuple(explanation_senses), tuple(section_senses) )
            #return next(iter(section_senses), None)

            #
            for e, s in matches:
                if e == explanation_sense_txt:
                    return s
