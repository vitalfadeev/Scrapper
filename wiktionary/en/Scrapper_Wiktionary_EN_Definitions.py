# new version
from ..Scrapper_Wiktionary_Checkers import *


IsMale = {
    in_template: {
        'g': {
            in_any_arg: {
                '*': { value_equal: { 'm', 'm-p' } }
            }
        },
        'masculine plural past participle of': {},
        'masculine plural of': {},
    },
    if_explanation: {
        text_contain: { "(usually male)" }
    }
}

IsFeminine = {
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
}

IsNeutre = {}

IsSingle = {
    in_template: {
        ('accusative singular of', 'dative singular of', 'en-archaic second-person singular of', 'en-archaic second-person singular past of', 'en-archaic third-person singular of', 'en-third person singular of', 'en-third-person singular of', 'enm-first-person singular of', 'enm-first/third-person singular past of', 'enm-second-person singular of', 'enm-second-person singular past of', 'enm-singular subjunctive of', 'enm-singular subjunctive past of', 'enm-third-person singular of', 'feminine singular of', 'feminine singular past participle of', 'genitive singular definite of', 'genitive singular indefinite of', 'genitive singular of', 'neuter singular of', 'neuter singular past participle of', 'sco-third-person singular of', 'singular definite of', 'singular indefinite of', 'singular of', 'vocative singular of'): {},
        "fi-form of": { in_arg: { "pl": { value_equal: "singular" } } }
    }
    # en-noun -> (s, p) -> s == self.label
}

IsPlural = {
    in_template: {
        'fi-form of': { in_arg: { 'pl': { value_equal: { 'plural'  } } } },
        'en-plural noun': {}
    }
}

SingleVariant = {
    in_template: { 'en-plural noun': { in_arg: { 'sg' } } }
}

PluralVariant = {
    in_template: {
        'en-noun': { en_noun: {} },
        'en-proper noun': { in_arg: { 0 } }
    }
    # en-noun -> (s, p) -> if (p != self.label): yield p
}

MaleVariant = {}

FemaleVariant = {}

IsVerbPast = {
    in_template: {
        'fi-form of': { in_arg: { 'tense': { value_equal: { 'past' } } } }
    }
}

IsVerbPresent = {
    in_template: {
        'fi-form of': { in_arg: { 'tense': { value_equal: { "present", "present connegative" } } } }
    }
}

IsVerbFutur = {}

Conjugation = {
    in_template: {
        'en-verb': { en_verb: {} }
    }
}

Synonymy = {
    in_section: {
        ( 'synonym', 'synonyms' ): {
            in_template: {
                ('syn', 'synonyms'): {
                    with_lang: {
                        'en': {
                            in_all_positional_args_except_lang: {}
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
            in_link: {},
        }
    },
    in_template: {
        ('syn', 'synonyms'): {
            with_lang: {
                'en': {
                    in_all_positional_args_except_lang: { }
                },
            },
        },
    },
}

Antonymy = {
    in_template: {
        ('antonyms', 'ant'): {
            with_lang: {
                'en': {
                    in_all_positional_args_except_lang: { }
                },
            },
        },
    },
    in_section: {
        ('antonym', 'antonyms'): {
            in_template: {
                ('antonyms', 'ant', 'l', 'lb', 'lbl', 'label', 'm', 'mention', 'link', 'wikipedia'): {
                    with_lang: {
                        'en': {
                            in_arg: { 1 }
                        },
                    },
                },
                'taxlink': {
                    in_arg: { 0 }
                },
                'vern': {
                    in_arg: { 0 }
                },
            },
            in_link: {},
        }
    }
}

Hypernymy = {
    in_template: {
        'hypernyms': {
            with_lang: {
                'en': {
                    in_all_positional_args_except_lang: { }
                }
            }
        }
    },
    in_section: {
        'hypernyms': {
            in_template: {
                ('hypernyms', 'l', 'lb', 'lbl', 'label', 'm', 'mention', 'link', 'wikipedia'): {
                    with_lang: {
                        'en': {
                            in_arg: { 1 }
                        },
                    },
                },
                'taxlink': {
                    in_arg: { 0 }
                },
                'vern'   : {
                    in_arg: { 0 }
                },
            },
            in_link: {},
        }
    }
}

Hyponymy = {
    in_template: {
        'hyponyms': {
            with_lang: {
                'en': {
                    in_all_positional_args_except_lang: { }
                }
            }
        }
    },
    in_section: {
        'hyponyms': {
            in_template: {
                ('hyponyms', 'l', 'lb', 'lbl', 'label', 'm', 'mention', 'link', 'wikipedia'): {
                    with_lang: {
                        'en': {
                            in_arg: { 1 }
                        },
                    },
                },
                'taxlink': {
                    in_arg: { 0 }
                },
                'vern'   : {
                    in_arg: { 0 }
                },
            },
            in_link: {},
        }
    }
}

Meronymy = {
    in_template: {
        'meronyms': {
            with_lang: {
                'en': {
                    in_all_positional_args_except_lang: { }
                }
            }
        }
    },
    in_section: {
        'meronyms': {
            in_template: {
                ('meronyms', 'l', 'lb', 'lbl', 'label', 'm', 'mention', 'link', 'wikipedia'): {
                    with_lang: {
                        'en': {
                            in_arg: { 1 }
                        },
                    },
                },
                'taxlink': {
                    in_arg: { 0 }
                },
                'vern'   : {
                    in_arg: { 0 }
                },
            },
            in_link: {},
        }
    }
}

Holonymy = {
    in_template: {
        'holonyms': {
            with_lang: {
                'en': {
                    in_all_positional_args_except_lang: { }
                }
            }
        }
    },
    in_section: {
        'holonyms': {
            in_template: {
                ('holonyms', 'l', 'lb', 'lbl', 'label', 'm', 'mention', 'link', 'wikipedia'): {
                    with_lang: {
                        'en': {
                            in_arg: { 1 }
                        },
                    },
                },
                'taxlink': {
                    in_arg: { 0 }
                },
                'vern'   : {
                    in_arg: { 0 }
                },
            },
            in_link: {},
        }
    }
}

Troponymy = {
    in_template: {
        'troponyms': {
            with_lang: {
                'en': {
                    in_all_positional_args_except_lang: { }
                }
            }
        }
    },
    in_section: {
        'troponyms': {
            in_template: {
                ('troponyms', 'l', 'lb', 'lbl', 'label', 'm', 'mention', 'link', 'wikipedia'): {
                    with_lang: {
                        'en': {
                            in_arg: { 1 }
                        },
                    },
                },
                'taxlink': {
                    in_arg: { 0 }
                },
                'vern'   : {
                    in_arg: { 0 }
                },
            },
            in_link: {},
        }
    }
}

Otherwise = {}

AlternativeFormsOther = {
    in_section: {
        'alternative forms': {
            in_template: {
                ('l', 'link'): {
                    with_lang: {
                        'en': {
                            in_arg: {1}
                        }
                    }
                }
            }
        }
    },
    in_template: {
        ('en-adv','en-adj'): {
            en_adj: {}
        }
    }
}

RelatedTerms = {
    in_section: {
        'related terms': {
            in_template: {
                ('l', 'link'): {
                    with_lang: {
                        'en': {
                            in_arg: { 1 }
                        }
                    }
                }
            },
            in_link: {},
        }
    },
    in_template: {
        ('see', 'also' ): { in_arg: { 1, 2, 3, 4, 5, 6, 7 } },
        ('cog', 'cognate'): {
            with_lang: {
                'en': {
                    in_arg: { 1 }
                }
            }
        }
    }
}

Coordinate = {
    in_template: {
        'coordinate terms': { in_arg: { 1,2,3,4,5,6,7 } }
    },
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
}

Translation_EN = {}

Translation_FR = {
    in_trans_top: {
        'french': {
            in_template: {
                't': {
                    with_lang: {
                        'fr': {
                            in_arg: { 1 }
                        }
                    }
                },
                't+': {
                    with_lang: {
                        'fr': {
                            in_arg: { 1 }
                        }
                    }
                },
            }
        }
    }
}

Translation_DE = {
    in_trans_top: {
        'german': {
            in_template: {
                't' : {
                    with_lang: {
                        'de': {
                            in_arg: { 1 }
                        }
                    }
                },
                't+': {
                    with_lang: {
                        'de': {
                            in_arg: { 1 }
                        }
                    }
                },
            }
        }
    }
}

Translation_IT = {
    in_trans_top: {
        'italian': {
            in_template: {
                't': {
                    with_lang: {
                        'it': {
                            in_arg: { 1 }
                        }
                    }
                },
                't+': {
                    with_lang: {
                        'it': {
                            in_arg: { 1 }
                        }
                    }
                },
            }
        }
    }
}

Translation_ES = {
    in_trans_top: {
        'spanish': {
            in_template: {
                't': {
                    with_lang: {
                        'es': {
                            in_arg: { 1 }
                        }
                    }
                },
                't+': {
                    with_lang: {
                        'es': {
                            in_arg: { 1 }
                        }
                    }
                },
            }
        }
    }
}

Translation_RU = {
    in_trans_top: {
        'russian': {
            in_template: {
                't': {
                    with_lang: {
                        'ru': {
                            in_arg: { 1 }
                        }
                    }
                },
                't+': {
                    with_lang: {
                        'ru': {
                            in_arg: { 1 }
                        }
                    }
                },
            }
        }
    }

}

Translation_PT = {
    in_trans_top: {
        'portuguese': {
            in_template: {
                't': {
                    with_lang: {
                        'pt': {
                            in_arg: { 1 }
                        }
                    }
                },
                't+': {
                    with_lang: {
                        'pt': {
                            in_arg: { 1 }
                        }
                    }
                },
            }
        }
    }
}

Labels = {
    in_template: {
        ('lb', 'lbl', 'label'): {
            with_lang: {
                'en': {
                    in_arg: { 1, 2, 3, 4, 5, 6, 7, 8, 9 }
                }
            }
        }
    },
}

Categories = {
    in_template: {
        ('top', 'topic', 'topics', 'categorize'): {
            with_lang: {
                'en': {
                    in_arg: { 1, 2, 3, 4, 5, 6, 7, 8, 9 }
                }
            }
        }
    },
}

Cognates = {
    in_template: {
        'cog': { in_arg_by_lang: { 1 } }
    },
}

Mentions = {
    in_template: {
        ('m', 'mention'): { in_arg_by_lang: { 1 } }
    },
}

SeeAlso = {
    in_template: {
        ('lb', 'lbl', 'label', 'm', 'mention', 'l', 'link',): {
            with_lang: {
                'en': {
                    in_arg: { 1 }
                }
            }
        },
        ('see', 'also', 'see also'): {
            in_arg: { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 }
        }
    }
}

Accent = {
    in_template: {
        ('a', 'accent'): {
            in_arg: { 0, 1, 2, 3, 4, 5 }
        }
    }
}

Qualifier = {
    in_template: {
        ('q','qf',  'i', 'qual', 'qualifier'): {
            in_arg: { 0, 1, 2, 3, 4 }
        }
    }
}

SenseRaw = {
    in_template: {
        ('s','sense'): {
            in_arg: { 0 }
        }
    }
}

ExternalLinks = {
    in_template: {
        'soplink': {
            in_all_positional_args: { }
        },
        ('w', 'wikipedia'): {
            in_arg: { 0 }
        }
    }
}
