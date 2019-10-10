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
                            in_arg: { 1, 2, 3, 4, 5, 6, 7 }
                        },
                    },
                },
                'taxlink': {
                    in_arg: { 0 }
                },
                ('l', 'lb', 'lbl', 'label', 'm', 'mention', 'link', 'wikipedia'): {
                    with_lang: {
                        'en': {
                            in_arg: { 1 }
                        },
                    },
                },
            },
            in_link: 1,
        }
    },
    in_template: {
        ('syn', 'synonyms'): {
            with_lang: {
                'en': {
                    in_arg: { 1, 2, 3, 4, 5, 6, 7 }
                },
            },
        },
        'wikipedia': {
            with_lang: {
                'en': {
                    in_arg: { 1 }
                }
            }
        }
    },
}

Antonymy = {
    in_template: {
        ('antonyms', 'ant'): {
            with_lang: {
                'en': {
                    in_arg: { 1,2,3,4,5,6,7 }
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
                    in_arg: { 1, 2, 3, 4, 5, 6, 7 }
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
                    in_arg: { 1, 2, 3, 4, 5, 6, 7 }
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
                    in_arg: { 1, 2, 3, 4, 5, 6, 7 }
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
                    in_arg: { 1, 2, 3, 4, 5, 6, 7 }
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
                    in_arg: { 1, 2, 3, 4, 5, 6, 7 }
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
                ('lb', 'lb', 'label', 'm', 'mention', 'l', 'link'): {
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

Categories = {
    in_template: {
        ('lb', 'lbl', 'label'): {
            with_lang: {
                'en': {
                    in_arg: { 1 }
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

def _redefine( var ):
    to_append = {}
    to_remove = []

    for k ,v in var.items():
        if isinstance(k, tuple):
            to_append.update( dict.fromkeys(k, v) )
            to_remove.append( k )
        elif isinstance( v, dict ):
            _redefine( v )

    if to_remove:
        for r in to_remove:
            var.pop( r )
        var.update( to_append )


def redefine():
    """ Replace tuple() keys in vars with each element from tuple """
    for varname, var in globals().items():
        if varname[0].isupper():
            if isinstance(var, dict):
                _redefine( var )

redefine()

_syn_templates = {
    'syn',
    'synonyms',
    'synonym of',
}
_other_templates = {
    'taxlink',  #
    'C', 'topics', 'top', 'c',  #
    'IPAchar',
    'R:American Heritage Dictionary', 'R:AHD',
    'R:Dictionary.com',
    'R:OCD2',
    'R:ODS online',
    'R:RHCD',
    'a', 'accent',
    'alter',
    'attention',
    'categorize',
    'catlangname', 'cln',
    'checksense',
    'cite-web',  #
    'g',
    'gl-noun',
    'gloss',
    'head',
    'synonym of', 'syn of',  #
    'vern',  #
}

_other = [
    "hu-case",
    "i",
    "it-noun",
    "ja-l",
    "ja-r",
    "jump",
    "ko-l",
    "l",
    "l-nb",
    "l/hu",
    "l/sh/Latn",
    "la-i-j",
    "label",
    "lang",
    "lb",
    "link",
    "m",
    "nn-inf",
    "pedialite",
    "pedlink",
    "plural of",
    "projectlink",
    "q",
    "qf",
    "qual",
    "qualifier",
    "rfc",
    "s",
    "see",
    "see also",
    "seeSynonyms",
    "sense",
    "soplink",
    "syn",
    "syndiff",
    "synonym of",
    "taxlink",
    "tbot entry",
    "th-l",
    "top",
    "top2",
    "top3",
    "top4",
    "topic",
    "topics",
    "vern",
    "vi-l",
    "w",
    "wikipedia",
    "wikisaurus:movement",
    "wikispecies",
    "ws",
    "ws link",
    "zh-cat",
    "zh-dial",
    "zh-l",
]
