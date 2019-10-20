# new version
from wiktionary.Scrapper_Wiktionary_Checkers import *


IsMale = {
    (in_self, in_all_parent_sections): {  # noun / etymology / english
        in_template: {
            'g': {
                in_any_arg: {
                    '*': { value_equal: { 'm', 'm-p' } }
                }
            },
            'masculine plural past participle of': {},
            'masculine plural of': {},
        },
    },
    in_self: {
        text_contain: { "(usually male)" }
    }
}

IsFeminine = {
    (in_self, in_all_parent_sections): {  # noun / etymology / english
        in_template: {
            'g': {
                in_any_arg: {
                    '*': { value_equal: {'f', 'f-p'} }
                }
            },
            'feminine noun of': {},
            'feminine of':{},
            'feminine plural of': {},
            'feminine singular of': {},
        }
    },
    in_self: {
        text_contain: { "(usually female)" }
    }
}

IsNeutre = {}

IsSingle = {
    (in_self, in_all_parent_sections): {  # noun / etymology / english
        in_template: {
            ('accusative singular of', 'dative singular of', 'en-archaic second-person singular of', 'en-archaic second-person singular past of', 'en-archaic third-person singular of', 'en-third person singular of', 'en-third-person singular of', 'enm-first-person singular of', 'enm-first/third-person singular past of', 'enm-second-person singular of', 'enm-second-person singular past of', 'enm-singular subjunctive of', 'enm-singular subjunctive past of', 'enm-third-person singular of', 'feminine singular of', 'feminine singular past participle of', 'genitive singular definite of', 'genitive singular indefinite of', 'genitive singular of', 'neuter singular of', 'neuter singular past participle of', 'sco-third-person singular of', 'singular definite of', 'singular indefinite of', 'singular of', 'vocative singular of'): {},
            "fi-form of": { in_arg: { "pl": { value_equal: "singular" } } },
            'en-noun': { single_en_noun: { equal_label: {} } },
        }
    }
}

IsPlural = {
    (in_self, in_all_parent_sections): {  # noun / etymology / english
        in_template: {
            'fi-form of': { in_arg: { 'pl': { value_equal: { 'plural'  } } } },
            'en-plural noun': {},
            'en-noun': { plural_en_noun: { equal_label: { } } },
        }
    }
}

SingleVariant = {
    in_all_parent_sections: {  # noun / etymology / english
        in_template: {
            'en-plural noun': { in_arg: { 'sg' } },
            'en-noun': { single_en_noun: { } },
        }
    }
}

PluralVariant = {
    in_all_parent_sections: {  # noun / etymology / english
        in_template: {
            'en-noun': { plural_en_noun: {} },
            'en-proper noun': { in_arg: { 0 } }
        }
    }
}

MaleVariant = {}

FemaleVariant = {}

IsVerbPast = {
    in_all_parent_sections: {  # noun / etymology / english
        in_template: {
            'fi-form of': { in_arg: { 'tense': { value_equal: { 'past' } } } }
        }
    }
}

IsVerbPresent = {
    in_all_parent_sections: {  # noun / etymology / english
        in_template: {
            'fi-form of': { in_arg: { 'tense': { value_equal: { "present", "present connegative" } } } }
        }
    }
}

IsVerbFutur = {}

Conjugation = {
    in_template: {
        'en-verb': { en_verb: {} }
    }
}

Synonymy = {
    in_all_parent_sections: {               # noun / etymology / english
        in_section: {                       # synonyms
            ( 'synonym', 'synonyms' ): {
                by_sense: {
                    in_template: {
                        ('syn', 'synonyms', 'synonym of'): {
                            with_lang: {
                                'en': {
                                    in_all_positional_args_except_lang: { }
                                },
                            },
                        },
                        ('col', 'col1', 'col2', 'col3', 'col4'): {
                            with_lang: {
                                'en': {
                                    in_all_positional_args_except_lang: { }
                                },
                            },
                        },
                        ('l', 'lb', 'lbl', 'label', 'm', 'mention', 'link', 'wikipedia', 'alter', 'll'): {
                            with_lang: {
                                'en': {
                                    in_arg: { 1 }
                                },
                            },
                        },
                        ('taxlink', 'vern', 'ws', 'ws link'): {
                            in_arg: { 0 }
                        },
                    },
                    in_link: { },
                }
            }
        },
    },
    # (in_self, in_parent_explanations, in_parent_sections): {    # self examples, parent explanations, in tos, etymology, lang (without subsections)
   (in_self, in_all_parents): {
        in_examples: {                                          # child examples in parent explanation
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

Antonymy = {
    in_all_parent_sections: {               # noun / etymology / english
        in_section: {
            ('antonym', 'antonyms'): {
                by_sense: {
                    in_template: {
                        ('antonyms', 'antonym', 'ant'): {
                            with_lang: {
                                'en': {
                                    in_all_positional_args_except_lang: { }
                                },
                            },
                        },
                        ('col', 'col1', 'col2', 'col3', 'col4'): {
                            with_lang: {
                                'en': {
                                    in_all_positional_args_except_lang: { }
                                },
                            },
                        },
                        ('l', 'lb', 'lbl', 'label', 'm', 'mention', 'link', 'wikipedia', 'alter', 'll'): {
                            with_lang: {
                                'en': {
                                    in_arg: { 1 }
                                },
                            },
                        },
                        ('taxlink', 'vern', 'ws', 'ws link'): {
                            in_arg: { 0 }
                        },
                    },
                    in_link: { },
                }
            }
        }
    },
    (in_self, in_all_parents): {
        in_examples: {  # child examples in parent explanation
            in_template: {
                ('antonyms', 'antonym', 'ant'): {
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

Hypernymy = {
    in_all_parent_sections: {  # noun / etymology / english
        in_section: {
            ('hypernym', 'hypernyms'): {
                by_sense: {
                    in_template: {
                        ('hypernyms', 'hyper'): {
                            with_lang: {
                                'en': {
                                    in_all_positional_args_except_lang: { }
                                },
                            },
                        },
                        ('col', 'col1', 'col2', 'col3', 'col4'): {
                            with_lang: {
                                'en': {
                                    in_all_positional_args_except_lang: { }
                                },
                            },
                        },
                        ('l', 'lb', 'lbl', 'label', 'm', 'mention', 'link', 'wikipedia', 'alter', 'll'): {
                            with_lang: {
                                'en': {
                                    in_arg: { 1 }
                                },
                            },
                        },
                        ('taxlink', 'vern', 'ws', 'ws link'): {
                            in_arg: { 0 }
                        },
                    },
                    in_link: { },
                }
            }
        }
    },
    (in_self, in_all_parents): {
        in_examples: {  # child examples in parent explanation
            in_template: {
                ('hypernyms', 'hyper'): {
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

Hyponymy = {
    in_all_parent_sections: {               # noun / etymology / english
        in_section: {                       # synonyms
            'hyponyms': {
                by_sense: {
                    in_template: {
                        ('hypo', 'hyponyms'): {
                            with_lang: {
                                'en': {
                                    in_all_positional_args_except_lang: { }
                                },
                            },
                        },
                        ('col', 'col1', 'col2', 'col3', 'col4'): {
                            with_lang: {
                                'en': {
                                    in_all_positional_args_except_lang: { }
                                },
                            },
                        },
                        ('l', 'lb', 'lbl', 'label', 'm', 'mention', 'link', 'wikipedia', 'alter', 'll'): {
                            with_lang: {
                                'en': {
                                    in_arg: { 1 }
                                },
                            },
                        },
                        ('taxlink', 'vern', 'ws', 'ws link'): {
                            in_arg: { 0 }
                        },
                    },
                    in_link: { },
                }
            }
        },
    },
    # (in_self, in_parent_explanations, in_parent_sections): {    # self examples, parent explanations, in tos, etymology, lang (without subsections)
   (in_self, in_all_parents): {
        in_examples: {                                          # child examples in parent explanation
            in_template: {
                ('hypo', 'hyponyms'): {
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

Meronymy = {
    in_all_parent_sections: {  # noun / etymology / english
        in_section: {
            'meronyms': {
                by_sense: {
                    in_template: {
                        'meronyms': {
                            with_lang: {
                                'en': {
                                    in_all_positional_args_except_lang: { }
                                },
                            },
                        },
                        ('col', 'col1', 'col2', 'col3', 'col4'): {
                            with_lang: {
                                'en': {
                                    in_all_positional_args_except_lang: { }
                                },
                            },
                        },
                        ('l', 'lb', 'lbl', 'label', 'm', 'mention', 'link', 'wikipedia', 'alter', 'll'): {
                            with_lang: {
                                'en': {
                                    in_arg: { 1 }
                                },
                            },
                        },
                        ('taxlink', 'vern', 'ws', 'ws link'): {
                            in_arg: { 0 }
                        },
                    },
                    in_link: { },
                }
            }
        }
    },
    (in_self, in_all_parents): {
        in_examples: {  # child examples in parent explanation
            in_template: {
                'meronyms': {
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

Holonymy = {
    in_all_parent_sections: {  # noun / etymology / english
        in_section: {
            'holonyms': {
                by_sense: {
                    in_template: {
                        'holonyms': {
                            with_lang: {
                                'en': {
                                    in_all_positional_args_except_lang: { }
                                },
                            },
                        },
                        ('col', 'col1', 'col2', 'col3', 'col4'): {
                            with_lang: {
                                'en': {
                                    in_all_positional_args_except_lang: { }
                                },
                            },
                        },
                        ('l', 'lb', 'lbl', 'label', 'm', 'mention', 'link', 'wikipedia', 'alter', 'll'): {
                            with_lang: {
                                'en': {
                                    in_arg: { 1 }
                                },
                            },
                        },
                        ('taxlink', 'vern', 'ws', 'ws link'): {
                            in_arg: { 0 }
                        },
                    },
                    in_link: { },
                }
            }
        }
    },
    (in_self, in_all_parents): {
        in_examples: {  # child examples in parent explanation
            in_template: {
                'holonyms': {
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

Troponymy = {
    in_all_parent_sections: {  # noun / etymology / english
        in_section: {
            'troponyms': {
                by_sense: {
                    in_template: {
                        'troponyms': {
                            with_lang: {
                                'en': {
                                    in_all_positional_args_except_lang: { }
                                },
                            },
                        },
                        ('col', 'col1', 'col2', 'col3', 'col4'): {
                            with_lang: {
                                'en': {
                                    in_all_positional_args_except_lang: { }
                                },
                            },
                        },
                        ('l', 'lb', 'lbl', 'label', 'm', 'mention', 'link', 'wikipedia', 'alter', 'll'): {
                            with_lang: {
                                'en': {
                                    in_arg: { 1 }
                                },
                            },
                        },
                        ('taxlink', 'vern', 'ws', 'ws link'): {
                            in_arg: { 0 }
                        },
                    },
                    in_link: { },
                }
            }
        }
    },
    (in_self, in_all_parents): {
        in_examples: {  # child examples in parent explanation
            in_template: {
                'troponyms': {
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

Otherwise = {}

AlternativeFormsOther = {
    in_all_parent_sections: {  # noun / etymology / english
        in_section: {
            ('alternative forms', 'alternate forms', 'alternative form', 'alterantive forms', 'Alternattive forms'): {
                in_template: {
                    ('l', 'lb', 'lbl', 'label', 'm', 'mention', 'link', 'wikipedia', 'alter', 'll'): {
                        with_lang: {
                            'en': {
                                in_arg: { 1 }
                            },
                        },
                    },
                    ('taxlink', 'vern', 'ws', 'ws link'): {
                        in_arg: { 0 }
                    },
                }
            }
        },
        in_template: {
            ('en-adv','en-adj'): {
                en_adj: {}
            }
        }
    }
}

RelatedTerms = {
    in_all_parent_sections: {  # noun / etymology / english
        in_section: {
            'related terms': {
                in_template: {
                    ('l', 'lb', 'lbl', 'label', 'm', 'mention', 'link', 'wikipedia', 'alter', 'll'): {
                        with_lang: {
                            'en': {
                                in_arg: { 1 }
                            },
                        },
                    },
                    ('taxlink', 'vern', 'ws', 'ws link'): {
                        in_arg: { 0 }
                    },
                    ('rel1', 'rel2', 'rel3', 'rel4', 'rel', 'der1', 'der2', 'der3', 'der4', 'der', ): {
                        with_lang: {
                            'en': {
                                in_all_positional_args_except_lang: {}
                            },
                        },
                    },
                },
                in_link: {},
            }
        },
    }
}

DerivedTerms = {
    in_all_parent_sections: {  # noun / etymology / english
        in_section: {
            'derived terms': {
                in_template: {
                    ('rel1', 'rel2', 'rel3', 'rel4', 'rel', 'der1', 'der2', 'der3', 'der4', 'der', ): {
                        with_lang: {
                            'en': {
                                in_all_positional_args_except_lang: {}
                            },
                        },
                    },
                    ('l', 'lb', 'lbl', 'label', 'm', 'mention', 'link', 'wikipedia', 'alter', 'll'): {
                        with_lang: {
                            'en': {
                                in_arg: { 1 }
                            },
                        },
                    },
                },
                in_link: {},
            }
        },
    }
}

Coordinate = {
    in_all_parent_sections: {  # noun / etymology / english
        in_section: {
            'coordinate terms': {
                in_template: {
                    ('lb', 'lbl', 'label', 'm', 'mention', 'l', 'link'): {
                        with_lang: {
                            'en': {
                                in_arg: { 1 }
                            }
                        }
                    }
                }
            }
        }
    },
    (in_self, in_all_parents): {
        in_template: {
            'coordinate terms': { in_arg: { 1, 2, 3, 4, 5, 6, 7 } }
        },
    },
}

Translation_EN = {}

Translation_FR = {
    in_all_parent_sections: {  # noun / etymology / english
        in_section: {
            'translations': {
                by_sense: {
                    in_language: {
                        'french': {
                            in_template: {
                                't' : { with_lang: { 'fr': { in_t: { 1 } } } },
                                't+': { with_lang: { 'fr': { in_t: { 1 } } } },
                            }
                        }
                    }
                }
            }
        }
    }
}

Translation_DE = {
    in_all_parent_sections: {  # noun / etymology / english
        in_section: {
            'translations': {
                by_sense: {
                    in_language: {
                        'german': {
                            in_template: {
                                't' : { with_lang: { 'de': { in_t: {} } } },
                                't+': { with_lang: { 'de': { in_t: {} } } },
                            }
                        }
                    }
                }
            }
        }
    }
}

Translation_IT = {
    in_all_parent_sections: {  # noun / etymology / english
        in_section: {
            'translations': {
                by_sense: {
                    in_language: {
                        'italian': {
                            in_template: {
                                't' : { with_lang: { 'it': { in_t: { 1 } } } },
                                't+': { with_lang: { 'it': { in_t: { 1 } } } },
                            }
                        }
                    }
                }
            }
        }
    }
}

Translation_ES = {
    in_all_parent_sections: {  # noun / etymology / english
        in_section: {
            'translations': {
                by_sense: {
                    in_language: {
                        'spanish': {
                            in_template: {
                                't' : { with_lang: { 'es': { in_t: { 1 } } } },
                                't+': { with_lang: { 'es': { in_t: { 1 } } } },
                            }
                        }
                    }
                }
            }
        }
    }
}

Translation_RU = {
    in_all_parent_sections: {  # noun / etymology / english
        in_section: {
            'translations': {
                by_sense: {
                    in_language: {
                        'russian': {
                            in_template: {
                                't' : { with_lang: { 'ru': { in_t: { 1 } } } },
                                't+': { with_lang: { 'ru': { in_t: { 1 } } } },
                            }
                        }
                    }
                }
            }
        }
    }
}

Translation_PT = {
    in_all_parent_sections: {  # noun / etymology / english
        in_section: {
            'translations': {
                by_sense: {
                    in_language: {
                        'portuguese': {
                            in_template: {
                                't' : { with_lang: { 'pt': { in_t: { 1 } } } },
                                't+': { with_lang: { 'pt': { in_t: { 1 } } } },
                            }
                        }
                    }
                }
            }
        }
    }
}

Labels = {
    (in_self, in_examples): {  # noun / etymology / english
        in_template: {
            ('lb', 'lbl', 'label'): {
                with_lang: {
                    'en': {
                        in_arg: { 1, 2, 3, 4, 5, 6, 7, 8, 9 }
                    }
                }
            }
        },
    },
}

Categories = {
    (in_self, in_all_parent_sections): {  # noun / etymology / english
        in_template: {
            ('top', 'topic', 'topics', 'categorize'): {
                with_lang: {
                    'en': {
                        in_arg: { 1, 2, 3, 4, 5, 6, 7, 8, 9 }
                    }
                }
            }
        }
    },
}

Cognates = {
    in_all_parent_sections: {  # noun / etymology / english
        in_template: {
            'cog': { in_arg_by_lang: { 1 } }
        },
    },
}

Mentions = {
    in_all_parent_sections: {  # noun / etymology / english
        in_template: {
            ('m', 'mention'): { in_arg_by_lang: { 1 } }
        },
    },
}

SeeAlso = {
    (in_self, in_all_parents): {  # noun / etymology / english / root
        in_section: {
            'see also': {
                in_template: {
                    ('l', 'link',): {
                        with_lang: {
                            'en': {
                                in_arg: { 1 }
                            }
                        }
                    },
                },
            },
            in_template: {
                ('see', 'also', 'see also'): {
                    in_arg: { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 }
                }
            }
        }
    }
}

Accent = {
    (in_self, in_all_parent_sections): {  # noun / etymology / english
        in_template: {
            ('a', 'accent'): {
                in_arg: { 0, 1, 2, 3, 4, 5 }
            }
        }
    }
}

Qualifier = {
    (in_self, in_all_parent_sections): {  # noun / etymology / english
        in_template: {
            ('q','qf',  'i', 'qual', 'qualifier'): {
                in_arg: { 0, 1, 2, 3, 4 }
            }
        }
    }
}

SenseRaw = {
    in_self: {  # noun / etymology / english
        in_template: {
            ('s','sense'): {
                in_arg: { 0 }
            }
        }
    }
}

ExternalLinks = {
    (in_self, in_all_parent_sections): {  # noun / etymology / english
        in_template: {
            'soplink': {
                in_all_positional_args: { }
            },
            ('w', 'wikipedia'): {
                in_arg: { 0 }
            },
            'pedia': {
                in_arg: { 0 }
            }
        }
    }
}
