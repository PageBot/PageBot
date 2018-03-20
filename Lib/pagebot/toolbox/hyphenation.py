# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     hyphenation/__init__.py
#
#     TODO
#     Add more languages
#     Include into text processing of PageBot (e.g. Flat text handling + reflow should become aware of ghost-hyphens)
#     Add scanning for combined words by recursively splitting into parts.
#     Add statistical hyphenation per language if words or combination of words fails.
#
#     Avaiable languages
#     "en"      English
#     "nl"      Dutch
#     "pt-br"   Portugese-Brasilian     Contributed by @filipenegrao
#
import os, codecs
from pagebot.contexts.platform import RESOURCES_PATH

DEFAULT_LANGUAGE = 'en'

# Key is language id (2 letters), value is dictionary of word-->hyphenated
languages = {} 

def hyphenatedWords(language=DEFAULT_LANGUAGE):
    u"""Answer the dictionary of hyphenated words for this language (default is English)."""
    if language not in languages:
        # Not initialized yet, try to read.
        path = RESOURCES_PATH + '/languages/%s.txt' % language
        if os.path.exists(path):
            languages[language] = words = {}
            f = codecs.open(path, mode="r", encoding="utf-8")
            hyphenatedLines = f.read().split('\n')
            f.close()
            for line in hyphenatedLines:
                if line.startswith('#'):
                    continue
                words[line.replace('-','')] = line
    return languages.get(language)

def hyphenate(word, language=DEFAULT_LANGUAGE, checkCombined=False):
    u"""Get the dictionary for the defined language and answer the hyphenated word if it exists.
    If it does not exists and checkCombined flag is True, try break the word into parts and check
    if on or nore of the parts are hyphenated. If all fails, then answer None.

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
    #
    # Dutch combination check:
    #
    # Word: marmerplaatsbepaling
    # Hyphenated: mar-mer-plaats-be-pa-ling
    #
    # Word: ochtendjaskledinghangerschroefdraad
    # Hyphenated: och-tend-jas-kle-ding-han-ger-schroef-draad
    #
    # Word: hagelslagroomboterbloemkoolstofzuigerveerpont
    # Hyphenated: ha-gel-slag-room-bo-ter-bloem-kool-stof-zui-ger-veer-pont

    hWords = hyphenatedWords(language) or {} # Empty dictionary if the langueage does not exist.
    hyphenated = hWords.get(word)
    if hyphenated is not None: # If exact, then stop searching.
        return hyphenated
    # In case the language support combined words, try to find matching parts.
    if checkCombined and len(word) > 4:
        # Checking on combined words (as in 'nl' and 'de').

        for i in range(4, len(word)-4):
            w1 = word[:i]
            hw1 = hyphenate(w1, language, True)
            if hw1 is None:
                continue
            w2 = word[i:]
            hw2 = hyphenate(w2, language, True)
            if hw2 is None:
                continue
            return hw1 + '-' + hw2
    return None

def words(language=DEFAULT_LANGUAGE):
    u"""Answer the sorted list of all words in the dictionary for this language."""
    return sorted(hyphenatedWords(language).keys())

def wordsByLength(language=DEFAULT_LANGUAGE):
    u"""Answer the dictionary with lists of words, groups by their length as key."""
    wordsByLength = {}
    for word in words(language):
        l = len(word)
        if not l in wordsByLength:
            wordsByLength[l] = []
        wordsByLength[l].append(word)
    return wordsByLength
    


if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

