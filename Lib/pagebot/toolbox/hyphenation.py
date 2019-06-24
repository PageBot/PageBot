# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
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
#     AvaiLable languages
#     "en"      English
#     "nl"      Dutch
#     "pt-br"   Portugese-Brasilian     Contributed by @filipenegrao
#     "dk"      Danish                  Contributed by Torben Wilhemsem
#     For other ISO language codes, see pagebot.constants
#
#     For English hyphenation words: 
#     https://www.hyphenation24.com/?term=xxxx
#
import os, codecs
from pagebot import getResourcesPath
from pagebot.constants import DEFAULT_LANGUAGE

# Key is language id (2 letters), value is dictionary of word-->hyphenated
languages = {}

def reset():
    global languages
    languages = {}

def hyphenatedWords(language=DEFAULT_LANGUAGE):
    """Answers the dictionary of hyphenated words for this language (default is English)."""
    if language not in languages:
        # Not initialized yet, try to read.
        path = getResourcesPath() + '/languages/%s.txt' % language
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
    """Get the dictionary for the defined language and answer the hyphenated
    word if it exists.  If it does not exists and checkCombined flag is True,
    try break the word into parts and check if on or nore of the parts are
    hyphenated. If all fails, then answer None.

    >>> from pagebot.constants import LANGUAGE_EN, LANGUAGE_NL, LANGUAGE_DK, LANGUAGE_PT_BR
    >>> len(hyphenatedWords(LANGUAGE_EN)) # English hyphenated words in the library
    172365
    >>> len(hyphenatedWords(LANGUAGE_NL)) # Dutch hyphenated words in the library
    235900
    >>> len(hyphenatedWords(LANGUAGE_PT_BR)) # Brazil-Portugeese hyphenated words in the library
    27437
    >>> len(hyphenatedWords(LANGUAGE_DK)) # Danish hyphenated words in the library
    183426
    >>> # E N G L I S H
    >>> hyphenate('housing', LANGUAGE_EN)
    'hous-ing'
    >>> # Single English words
    >>> hyphenate('Tutankhamun'), hyphenate('Tutankhamun', LANGUAGE_EN) # English is default
    ('Tut-ankh-a-mun', 'Tut-ankh-a-mun')
    >>> # D U T C H Typically testing the hyphenation of combined Dutch words
    >>> hyphenate('marmerplaatjes', LANGUAGE_NL)
    'mar-mer-plaat-jes'
    >>> # Hyphenates as plaat-staal (sheet of steel) where plaats-taal (regional language) also would have been valid
    >>> hyphenate('plaatstaal', LANGUAGE_NL)
    'plaat-staal'
    >>> # Combined dutch words, hyphenating between valid words.
    >>> hyphenate('marmer', LANGUAGE_NL)
    'mar-mer'
    >>> hyphenate('plaats', LANGUAGE_NL)
    'plaats'
    >>> hyphenate('marmerplaats', LANGUAGE_NL) is None # Without recursively searching combinations, does not find this word..
    True
    >>> hyphenate('marmerplaats', LANGUAGE_NL, True) # Find combination (slower), although the word itself is not part of the library.
    'mar-mer-plaats'
    >>> hyphenate('marmerplaatsbepaling', LANGUAGE_NL, True)
    'mar-mer-plaats-be-pa-ling'
    >>> hyphenate('ochtendjaskledinghangerschroefdraad', LANGUAGE_NL, True)
    'och-tend-jas-kle-ding-han-ger-schroef-draad'
    >>> hyphenate('hagelslagroomboterbloemkoolstofzuigerveerpont', LANGUAGE_NL, True)
    'ha-gel-slag-room-bo-ter-bloem-kool-stof-zui-ger-veer-pont'
    >>> # Longest in practice. Don't go longer than this, as calculation time exponentioally increases.
    >>> hyphenate('kernenergieadviesbureaugebouwtoegangsdeurknopbedieningspaneeltjes', LANGUAGE_NL, True)
    'kern-ener-gie-ad-vies-bu-reau-ge-bouw-toe-gangs-deur-knop-be-die-nings-pa-neel-tjes'
    >>> hyphenate('housewarmingpartyinvitation', LANGUAGE_NL, True) is None # --> None: no matching in another language.
    True
    >>> hyphenate('housewarmingpartyinvitation', LANGUAGE_EN, True) # --> Still works: house-warm-ing-par-ty-in-vi-ta-tion
    'house-warm-ing-par-ty-in-vi-ta-tion'
    >>> # First [100:105] words of the sorted list of all language words in the dictionary.
    >>> words('nl')[100:105]
    ['aanaardt', 'aanademing', 'aanbad', 'aanbak', 'aanbakken']
    >>> # P O R T U G E S E
    >>> hyphenate('abarcar', LANGUAGE_PT_BR)
    'a-bar-car'
    >>> hyphenate('cefalorraquidiano', LANGUAGE_PT_BR)
    'ce-fa-lor-ra-qui-di-a-no'
    >>> hyphenate('abarcarcefalorraquidiano', LANGUAGE_PT_BR, True)
    'a-bar-car-ce-fa-lor-ra-qui-di-a-no'
    """
    """
    TODO: Unicode not showing well in docTest feedback
    >>> # D A N I S H
    >>> hyphenate('adessiverne', LANGUAGE_DK)
    'ades-si-ver-ne'
    >>> hyphenate('ablationsområder', LANGUAGE_DK)
    'ab-la-tions-om-rå-der'
    >>> hyphenate('adfærdsforstyrrelse', LANGUAGE_DK)
    'ad-færds-for-styr-rel-se' """
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
    """Answers the sorted list of all words in the dictionary for this language."""
    return sorted(hyphenatedWords(language).keys())

def wordsByLength(language=DEFAULT_LANGUAGE):
    """Answers the dictionary with lists of words, groups by their length as key."""
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

