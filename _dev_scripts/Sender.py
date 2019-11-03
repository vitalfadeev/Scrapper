# !/usr/bin/python
# -*- coding: utf-8 -*-

import requests
"""
    This module will make a post request to the URL, as an argument it will pass a json file (dictionary)
    which will contain two keys: 'explanations' and 'translations', value of each will be a list of strings.
    
    * 'explanations' list will contain all the explanations of the word from DB
    * 'explanations' list will contain all the explanations of the word from DB
    * 'explanations' list will contain all the explanations of the word from DB
    
    * 'translations' list will contain all the {explanations of translations} to the word
    
    In result response will contain a json file (dictionary) which will have one key - 'result'
    the value of 'result' will be a list, each element of the list is another list, containing pairs of strings
    (Match_List_PKS_With_Lists_Of_PKS will try to match each explanation to its best translation explanation)
    first element will be explanation and second - corresponding explanation of translation
    
    If our function didn't find a matching explanation of translation then it will return a list:
    first element will be explanation and second - null
    
"""
url = 'http://lviv.ixioo.com:8030/Match_List_PKS_With_Lists_Of_PKS'
if 0:
    data = {
        'explanations':['A domesticated subspecies of feline animal, commonly kept as a house pet.',
                        'Any similar animal of the family Felidae, which includes lions, tigers, bobcats, etc. ',
                        'A spiteful or angry woman',
                        'An enthusiast or player of jazz.',
                        'A person (usually male).',
                        'A prostitute',
                        'A strong tackle used to hoist an anchor to the cathead of a ship',
                        "Short form of cat-o'-nine-tails. ",
                        'A sturdy merchant sailing vessel',
                        'The trap of the game of "trap and ball".',
                        'The pointed piece of wood that is struck in the game of tipcat.',
                        ' A vagina, a vulva; the female external genitalia.',
                        'A double tripod (for holding a plate, etc.) with six feet, of which three rest on the ground, in whatever position it is placed.',
                        'A wheeled shelter, used in the Middle Ages as a siege weapon to allow assailants to approach enemy defences.'
                        ],
        'translations': ['domestic species',
                        'member of the family Felidae',
                        'member of the subfamily Pantherinae',
                        'type of fish',
                        'jazz enthusiast',
                        'guy, fellow',
                        'strong tackle used to hoist an anchor to the cathead of a ship',
                        "cat-o'-nine-tails",
                        'type of boat ',
                        'game of "trap and ball" (or "cat and dog")',
                        'the trap in the game of "trap and ball"',
                        'wheeled shelter used as siege weapon'
                        ]
    }

    r = requests.post(url, json=data)
    print('Sent a request.')
    print("status_code:", r.status_code)
    print(r.text)

#
# Case 2
# source: https://en.wiktionary.org/wiki/cat#Verb
#
if 0:
    data2 = {
        'explanations': [
            "(nautical, transitive) To hoist (the anchor) by its ring so that it hangs at the cathead.",
            "(nautical, transitive) To flog with a cat-o'-nine-tails.",
            "(slang) To vomit something.",
            "To go wandering at night.",
            "To gossip in a catty manner.",
            ],
        'translations': [
            "raise anchor to cathead",
            "flog",
            "vomit",
            "",
            "",
        ]
    }

    r = requests.post(url, json=data2)
    print('Sent a request 2.')
    print("status_code:", r.status_code)
    print(r.text)

if 0:
	#
	# Case 3
	# source: https://en.wiktionary.org/wiki/word
	#
	data3 = {
		'explanations': [
			'The smallest unit of language that has a particular meaning and can be expressed by itself; the smallest discrete, meaningful unit of language. (contrast morpheme.)\n##*: Polonius: What do you read, my lord?\n## The smallest discrete unit of spoken language with a particular meaning, composed of one or more phonemes and one or more morphemes\n\n## The smallest discrete unit of written language with a particular meaning, composed of one or more letters or symbols and one or more morphemes\n##*: Polonius: What do you read, my lord?\n## A discrete, meaningful unit of language approved by an authority or native speaker (compare non-word).\n\n# Something like such a unit of language:\n\n## A sequence of letters, characters, or sounds, considered as a discrete entity, though it does not necessarily belong to a language or have a meaning\n\n## (telegraphy) A unit of text equivalent to five characters and one space. [from 19th c.]\n\n## (computing) A fixed-size group of bits handled as a unit by a machine (on many 16-bit machines, 16 bits or two bytes). [from 20th c.]\n\n## (computer science) A finite string that is not a command or operator. [from 20th or 21st c.]\n\n## (group theory) A group element, expressed as a product of group elements.\n\n# The fact or act of speaking, as opposed to taking action. [from 9th c.]\n\n# (now rare  outside certain phrases) Something that someone said; a comment, utterance; speech. [from 10th c.]\n#*: And Peter remembered the word of Jesus, which said unto him, Before the cock crow, thou shalt deny me thrice.\n# (obsolete  outside certain phrases) A watchword or rallying cry, a verbal signal (even when consisting of multiple words).\n#: mum\'s the word\n# (obsolete) A proverb or motto.\n\n\n#  News; tidings (used without an article). [from 10th c.]\n#*: Word had gone round during the day that old Major, the prize Middle White boar, had had a strange dream on the previous night and wished to communicate it to the other animals.\n# An order; a request or instruction; an expression of will. [from 10th c.]\n#: He sent word that we should strike camp before winter.\n# A promise; an oath or guarantee. [from 10th c.]\n\n#: I give you my word that I will be there on time.\n# A brief discussion or conversation. [from 15th c.]\n\n#: Can I have a word with you?\n# (in the plural) See words.\n\n#: There had been words between him and the secretary about the outcome of the meeting.\n# (theology, sometimes Word) Communication from God; the message of the Christian gospel; the Bible, Scripture. [from 10th c.]\n\n#: Her parents had lived in Botswana, spreading the word among the tribespeople.\n# (theology, sometimes Word) Logos, Christ. [from 8th c.]\n#*: And that worde was made flesshe, and dwelt amonge vs, and we sawe the glory off yt, as the glory off the only begotten sonne off the father, which worde was full of grace, and verite.\n# (transitive) To say or write (something) using particular words; to phrase (something).\n\n#: I’m not sure how to word this letter to the council.\n# (transitive, obsolete) To flatter with words, to cajole.\n\n# (transitive) To ply or overpower with words.\n\n# (transitive, rare) To conjure with a word.\n#*: Against him [...] who could word heaven and earth out of nothing, and can when he pleases word them into nothing again.\n# (intransitive, archaic) To speak, to use words; to converse, to discourse.\n\n# (slang, African American Vernacular) Truth, indeed, that is the truth! The shortened form of the statement "My word is my bond."\n\n#: "Yo, that movie was epic!" / "Word?" ("You speak the truth?") / "Word." ("I speak the truth.")\n# (slang, emphatic, stereotypically, African American Vernacular) An abbreviated form of word up; a statement of the acknowledgment of fact with a hint of nonchalant approval.\n\n# Alternative form of worth (to become).\n\n',
			'The smallest discrete unit of spoken language with a particular meaning, composed of one or more phonemes and one or more morphemes',
			'The smallest discrete unit of written language with a particular meaning, composed of one or more letters or symbols and one or more morphemes',
			'A discrete, meaningful unit of language approved by an authority or native speaker (compare non-word).',
			'Something like such a unit of language:',

			'A sequence of letters, characters, or sounds, considered as a discrete entity, though it does not necessarily belong to a language or have a meaning',
			'(telegraphy) A unit of text equivalent to five characters and one space. [from 19th c.]',
			'(computing) A fixed-size group of bits handled as a unit by a machine (on many 16-bit machines, 16 bits or two bytes). [from 20th c.]',
			'(computer science) A finite string that is not a command or operator. [from 20th or 21st c.]',
			'(group theory) A group element, expressed as a product of group elements.',

			'The fact or act of speaking, as opposed to taking action. [from 9th c.]',
			'(now rare  outside certain phrases) Something that someone said; a comment, utterance; speech. [from 10th c.]',
			'(obsolete  outside certain phrases) A watchword or rallying cry, a verbal signal (even when consisting of multiple words).',
			'(obsolete) A proverb or motto.',
			'',

			'An order; a request or instruction; an expression of will. [from 10th c.]',
			'A promise; an oath or guarantee. [from 10th c.]',
			'A brief discussion or conversation. [from 15th c.]',
			'(in the plural) See words.',
			'(theology, sometimes Word) Communication from God; the message of the Christian gospel; the Bible, Scripture. [from 10th c.]',

			'(theology, sometimes Word) Logos, Christ. [from 8th c.]'
		],
		'translations': [
			'news, tidings',
			'the word of God',
			'group theory: kind of group element',
			'promise',
			'discussion',

			'an angry debate; argument',
			'Christ',
			'computer science: finite string which is not a command or operator',
			'unit of language',
			'something which has been said',

			'computing: fixed-size group of bits handled as a unit',
			'telegraphy: unit of text',
			'',
			'',
			'',

			'',
			'',
			'',
			'',
			'',

			'',
		]
	}

	assert( len( data3['explanations']) == len( data3['translations']) )

	r = requests.post(url, json=data3)
	print('Sent a request 3.')
	print("status_code:", r.status_code)
	print(r.text)
	#print(r.json( encoding='UTF-8' ))


if 0:
	#
	# Case 4
	# source: https://en.wiktionary.org/wiki/pie
	#
	data4 = {
		'explanations': [
			'Letters or words, in writing or speech, that have no meaning or pattern or seem to have no meaning.', 
			'An untrue statement.', 
			'That which is silly, illogical and lacks any meaning, reason or value; that which does not make sense.', 
			'Something foolish.', 
			'(literature) A type of poetry that contains strange or surreal ideas, as, for example, that written by Edward Lear.', 
			'(biology) A damaged DNA sequence whose products are not biologically active, that is, that does nothing.'
		],
		'translations': [
			'type of poetry', 
			'untrue statement', 
			'damaged DNA sequence', 
			'meaningless words'
		]
	}
	r = requests.post(url, json=data4)
	print('Sent a request 4.')
	print("status_code:", r.status_code)
	print(r.text)

if 0:
	#
	# Case 5
	# source: https://en.wiktionary.org/wiki/name
	#
	data5 = {
		'explanations': ['(ditransitive) To give a name to.', '(transitive) To mention, specify.', '(transitive) To identify as relevant or important', '(transitive) To publicly implicate.', '(transitive) To designate for a role.', '(transitive, Westminster system politics) To initiate a process to temporarily remove a member of parliament who is breaking the rules of conduct.'],
		'translations': ['to publicly implicate', 'to give a name to', 'to mention, specify', 'to identify, define, specify', 'to designate for a role']
	}
	r = requests.post(url, json=data5)
	print('Sent a request 5.')
	print("status_code:", r.status_code)
	print(r.text)


if 0:
	#
	# Case 6
	# source: https://en.wiktionary.org/wiki/cat
	#
	data6 = {
		'explanations': [
			'A domesticated subspecies (Felis silvestris catus) of feline animal, commonly kept as a house pet. [from 8thc.]',
			'Any similar animal of the family Felidae, which includes lions, tigers, bobcats, etc.',
			'(offensive) A spiteful or angry woman. [from earlier 13thc.]',
			'An enthusiast or player of jazz.',
			'(slang) A person (usually male).',
			'(slang) A prostitute. [from at least early 15thc.]',
			'(nautical) A strong tackle used to hoist an anchor to the cathead of a ship.',
			"(chiefly nautical) Short form of cat-o'-nine-tails.",
			'(archaic) A sturdy merchant sailing vessel (now only in "catboat").',
			'The trap of the game of "trap and ball".',
			'(archaic) The pointed piece of wood that is struck in the game of tipcat.',
			'(slang, vulgar, African American Vernacular) A vagina, a vulva; the female external genitalia.',
			'A double tripod (for holding a plate, etc.) with six feet, of which three rest on the ground, in whatever position it is placed.',
			'(historical) A wheeled shelter, used in the Middle Ages as a siege weapon to allow assailants to approach enemy defences.',
			'(nautical, transitive) To hoist (the anchor) by its ring so that it hangs at the cathead.',
			"(nautical, transitive) To flog with a cat-o'-nine-tails.",
			'(slang) To vomit something.',
			'To go wandering at night.',
			'To gossip in a catty manner.',
			'A catamaran.',
			'(computing) A program and command in Unix that reads one or more files and directs their content to the standard output.',
			'(computing, transitive) To apply the cat command to (one or more files).',
			'(computing, slang) To dump large amounts of data on (an unprepared target) usually with no intention of browsing it carefully.',
			'(Ireland, informal) Terrible, disastrous.',
			'(slang) A street name of the drug methcathinone.',
			'(military, naval) A catapult.',
			'Abbreviation of category.',
			'Abbreviation of catfish.',
			'(slang) Any of a variety of earth-moving machines. (from their manufacturer Caterpillar Inc.)',
			'A caterpillar drive vehicle (a ground vehicle which uses caterpillar tracks), especially tractors, trucks, minibuses, and snow groomers.'
		],
		'translations': [
			'any member of the suborder (sometimes superfamily) Feliformia or Feloidea',
			'any member of the subfamily Felinae, genera Puma, Acinonyx, Lynx, Leopardus, and Felis)',
			'any member of the subfamily Pantherinae, genera Panthera, Uncia and Neofelis',
			'technically, all members of the genus Panthera',
			'any member of the extinct subfamily Machairodontinae, genera Smilodon, Homotherium, Miomachairodus, etc.'
		]
	}
	r = requests.post(url, json=data6)
	print('Sent a request 6.')
	print("status_code:", r.status_code)
	print(r.text)

if 1:
	#
	# Case 7
	# source: https://en.wiktionary.org/wiki/cat
	#
	# Hyponyms
	# ['A domesticated subspecies (Felis silvestris catus) of feline animal, commonly kept as a house pet. [from 8thc.]', 'Any similar animal of the family Felidae, which includes lions, tigers, bobcats, etc.', '(offensive) A spiteful or angry woman. [from earlier 13thc.]', 'An enthusiast or player of jazz.', '(slang) A person (usually male).', '(slang) A prostitute. [from at least early 15thc.]', '(nautical) A strong tackle used to hoist an anchor to the cathead of a ship.', "(chiefly nautical) Short form of cat-o'-nine-tails.", '(archaic) A sturdy merchant sailing vessel (now only in "catboat").', 'The trap of the game of "trap and ball".', '(archaic) The pointed piece of wood that is struck in the game of tipcat.', '(slang, vulgar, African American Vernacular) A vagina, a vulva; the female external genitalia.', 'A double tripod (for holding a plate, etc.) with six feet, of which three rest on the ground, in whatever position it is placed.', '(historical) A wheeled shelter, used in the Middle Ages as a siege weapon to allow assailants to approach enemy defences.', '(nautical, transitive) To hoist (the anchor) by its ring so that it hangs at the cathead.', "(nautical, transitive) To flog with a cat-o'-nine-tails.", '(slang) To vomit something.', 'To go wandering at night.', 'To gossip in a catty manner.', 'A catamaran.', '(computing) A program and command in Unix that reads one or more files and directs their content to the standard output.', '(computing, transitive) To apply the cat command to (one or more files).', '(computing, slang) To dump large amounts of data on (an unprepared target) usually with no intention of browsing it carefully.', '(Ireland, informal) Terrible, disastrous.', '(slang) A street name of the drug methcathinone.', '(military, naval) A catapult.', 'Abbreviation of category.', 'Abbreviation of catfish.', '(slang) Any of a variety of earth-moving machines. (from their manufacturer Caterpillar Inc.)', 'A caterpillar drive vehicle (a ground vehicle which uses caterpillar tracks), especially tractors, trucks, minibuses, and snow groomers.']
	# ['domestic species']
	#
	data7 = {
		'explanations': [
			'A domesticated subspecies (Felis silvestris catus) of feline animal, commonly kept as a house pet. [from 8thc.]',
			'Any similar animal of the family Felidae, which includes lions, tigers, bobcats, etc.',
			'(offensive) A spiteful or angry woman. [from earlier 13thc.]', 'An enthusiast or player of jazz.',
			'(slang) A person (usually male).', '(slang) A prostitute. [from at least early 15thc.]',
			'(nautical) A strong tackle used to hoist an anchor to the cathead of a ship.',
			"(chiefly nautical) Short form of cat-o'-nine-tails.",
			'(archaic) A sturdy merchant sailing vessel (now only in "catboat").',
			'The trap of the game of "trap and ball".',
			'(archaic) The pointed piece of wood that is struck in the game of tipcat.',
			'(slang, vulgar, African American Vernacular) A vagina, a vulva; the female external genitalia.',
			'A double tripod (for holding a plate, etc.) with six feet, of which three rest on the ground, in whatever position it is placed.',
			'(historical) A wheeled shelter, used in the Middle Ages as a siege weapon to allow assailants to approach enemy defences.',
			'(nautical, transitive) To hoist (the anchor) by its ring so that it hangs at the cathead.',
			"(nautical, transitive) To flog with a cat-o'-nine-tails.", '(slang) To vomit something.',
			'To go wandering at night.', 'To gossip in a catty manner.', 'A catamaran.',
			'(computing) A program and command in Unix that reads one or more files and directs their content to the standard output.',
			'(computing, transitive) To apply the cat command to (one or more files).',
			'(computing, slang) To dump large amounts of data on (an unprepared target) usually with no intention of browsing it carefully.',
			'(Ireland, informal) Terrible, disastrous.', '(slang) A street name of the drug methcathinone.',
			'(military, naval) A catapult.', 'Abbreviation of category.', 'Abbreviation of catfish.',
			'(slang) Any of a variety of earth-moving machines. (from their manufacturer Caterpillar Inc.)',
			'A caterpillar drive vehicle (a ground vehicle which uses caterpillar tracks), especially tractors, trucks, minibuses, and snow groomers.' ],
		'translations': [ 'domestic species' ]
	}
	r = requests.post(url, json=data7)
	print('Sent a request 7.')
	print("status_code:", r.status_code)
	print(r.text)

