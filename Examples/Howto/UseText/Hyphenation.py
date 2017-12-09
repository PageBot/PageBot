# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     Hyphenation.py
#
from pagebot.toolbox.hyphenation import hyphenate, hyphenatedWords, words

print 'English hyphenated words:', len(hyphenatedWords('en'))
print 'Dutch hyphenated words:', len(hyphenatedWords('nl'))

print hyphenate('housing', 'en')
print hyphenate('Tutankhamun') # English is default
print hyphenate('Tutankhamun', 'en')

print hyphenate('marmerplaatjes', 'nl')
# Hyphenates as plaat-staal (sheet of steel) where plaats-taal (regional language) also would have been valid
print hyphenate('plaatstaal', 'nl') 

# Combined dutch words, hyphenating between valid words.
print hyphenate('marmer', 'nl', True)
print hyphenate('plaats', 'nl', True)
print hyphenate('marmerplaats', 'nl', True)
print hyphenate('marmerplaatsbepaling', 'nl', True)
print hyphenate('ochtendjaskledinghangerschroefdraad', 'nl', True)
print hyphenate('hagelslagroomboterbloemkoolstofzuigerveerpont', 'nl', True)

# First 20 words of the sorted list of all language words in the dictionary.
print words('nl')[:20] 
