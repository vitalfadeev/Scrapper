import string

table = str.maketrans( dict.fromkeys( string.punctuation ) )

def isEnglish(s):
    return s.translate( table ).isalnum()


print( isEnglish('slabiky, ale liší se podle významu') )
print( isEnglish('English') )
print( isEnglish('ގެ ފުރަތަމަ ދެ އަކުރު ކަ') )
print( isEnglish('how about this one : 通 asfަ') )
print( isEnglish('?fd4))45s&') )
print( isEnglish('Текст на русском') )
