import string

ASCII           = set(string.printable)

def is_ascii( s ):
    for c in s:
        if c not in ASCII:
            return False

    return True


print( is_ascii('slabiky, ale liší se podle významu') )
print( is_ascii('English') )
print( is_ascii('ގެ ފުރަތަމަ ދެ އަކުރު ކަ') )
print( is_ascii('how about this one : 通 asfަ') )
print( is_ascii('?fd4))45s&') )
print( is_ascii('Текст на русском') )
print( is_ascii('English sentence with spaces and dot.') )
