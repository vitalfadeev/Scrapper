from wiktionary.Scrapper_Wiktionary_Checkers import *

Synonymy = {
    in_each_parent_section: {               # noun / etymology / english
        in_section: {                       # synonyms
            ( 'synonym', 'synonyms' ): {
                if_single_explanation: {    # skip sense detection
                    checkers_from: [ 'Synonymy', if_explanation, in_each_parent_section, in_section, 'synonyms', if_many_explanations, get_senses, in_li ]
                },
                if_many_explanations: {
                    # extract senses
                    # get_senses: {           # extract senses. senes[ sense ] = [ lexem, lexem ]
                    #     in_li: {
                    #         in_template: {
                    #             'sense': {
                    #                 in_arg: { 0 }
                    #             }
                    #         }
                    #     }
                    # },
                    # extract senses
                    # pks match
                    #   all explanations + all synonyms senses
                    #   cache matches
                    #
                    # here have: synonyms senses, explanation sense, matched pairs
                    # match:
                    #   have synonym_sense + explanation_sense
                    #   sense
                    in_sense_en_synonyms: {
                        in_template: {
                            ('syn', 'synonyms'): {
                                with_lang: {
                                    'en': {
                                        in_all_positional_args_except_lang: { }
                                    },
                                },
                            },
                            'taxlink': {
                                in_arg: { 0 }
                            },
                            'vern': {
                                in_arg: { 0 }
                            },
                            ('ws', 'ws link'): {
                                in_arg: { 0 }
                            },
                            ('l', 'lb', 'lbl', 'label', 'm', 'mention', 'link', 'wikipedia', 'synonym of', 'alter'): {
                                with_lang: {
                                    'en': {
                                        in_arg: { 1 }
                                    },
                                },
                            },
                        },
                        in_link: { },
                    }
                },

            }
        },
    },
    (in_self, in_parent_explanations, in_parent_sections): {    # self examples, parent explanations, in tos, etymology, lang (without subsections)
        in_examples: {                      # child examples in parent explanation
            in_template: {
                ('syn', 'synonyms'): {
                    with_lang: {
                        'en': {
                            in_all_positional_args_except_lang: { }
                        },
                    },
                },
            },
        },
    },
}

