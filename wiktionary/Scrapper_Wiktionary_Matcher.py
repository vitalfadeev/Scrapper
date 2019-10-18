import Scrapper_IxiooAPI

class Matcher:
    @classmethod
    def match( cls, explanation_sense_txt, explanation_senses, section_senses ):
        if section_senses and explanation_sense_txt:
            matches = Scrapper_IxiooAPI.Match_List_PKS_With_Lists_Of_PKS( tuple(explanation_senses), tuple(section_senses) )
            #return next(iter(section_senses), None)

            #
            for e, s in matches:
                if e == explanation_sense_txt:
                    return s
