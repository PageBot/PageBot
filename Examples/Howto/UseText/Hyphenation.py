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

def hyphenDemo(s, language='en'):
    u"""Show demo of hyphenation.

    >>> len(hyphenatedWords('en')) # English hyphenated words in the library
    171942
    >>> len(hyphenatedWords('nl')) # Dutch hyphenated words in the library
    235916
    >>> hyphenate('housing', 'en')
    u'hous-ing'
    >>> # Single English words
    >>> hyphenate('Tutankhamun'), hyphenate('Tutankhamun', 'en') # English is default
    (u'Tut-ankh-a-mun', u'Tut-ankh-a-mun')
    >>> # Combined Dutch words
    >>> hyphenate('marmerplaatjes', 'nl')
    u'mar-mer-plaat-jes'
    >>> # Hyphenates as plaat-staal (sheet of steel) where plaats-taal (regional language) also would have been valid
    >>> hyphenate('plaatstaal', 'nl') 
    u'plaat-staal'
    >>> # Combined dutch words, hyphenating between valid words.
    >>> hyphenate('marmer', 'nl', True)
    u'mar-mer'
    >>> hyphenate('plaats', 'nl', True)
    u'plaats'
    >>> hyphenate('marmerplaats', 'nl', True) # Find combination, although the word itself is not part of the library.
    u'mar-mer-plaats'
    >>> hyphenate('marmerplaatsbepaling', 'nl', True)
    u'mar-mer-plaats-be-pa-ling'
    >>> hyphenate('ochtendjaskledinghangerschroefdraad', 'nl', True)
    u'och-tend-jas-kle-ding-han-ger-schroef-draad'
    >>> hyphenate('hagelslagroomboterbloemkoolstofzuigerveerpont', 'nl', True)
    u'ha-gel-slag-room-bo-ter-bloem-kool-stof-zui-ger-veer-pont'
    >>> # Longest in practice. Don't go longer than this, as calculation time exponentioally increases.
    >>> hyphenate('kernenergieadviesbureaugebouwtoegangsdeurknopbedieningspaneeltjes', 'nl', True)
    u'kern-ener-gie-ad-vies-bu-reau-ge-bouw-toe-gangs-deur-knop-be-die-nings-pa-neel-tjes'
    >>> hyphenate('housewarmingpartyinvitation', 'nl', True) is None # --> None: no matching in another language.
    True
    >>> hyphenate('housewarmingpartyinvitation', 'en', True) # --> Still works: house-warm-ing-par-ty-in-vi-ta-tion
    u'house-warm-ing-par-ty-in-vi-ta-tion'
    >>> # First [100:105] words of the sorted list of all language words in the dictionary.
    >>> words('nl')[100:105] 
    [u'aanaardt', u'aanademing', u'aanbad', u'aanbak', u'aanbakken']
    """
    return hyphenate(s)


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
