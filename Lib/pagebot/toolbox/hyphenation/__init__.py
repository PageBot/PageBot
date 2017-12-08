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
import os, codecs
from pagebot import getRootPath

DEFAULT_LANGUAGE = 'en'

# Key is language id (2 letters), value is dictionary of word-->hyphenated
languages = {} 

def hyphenatedWords(language=DEFAULT_LANGUAGE):
    u"""Answer the dictionary of hyphenated words for this language (default is English)."""
    if not language in languages:
        # Not initialized yet, try to read.
        path = '%s/Lib/pagebot/toolbox/hyphenation/languages/%s.txt' % (getRootPath(), language)
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
    if on or nore of the parts are hyphenated. If all fails, then answer None."""
    #
    # Dutch combination check:
    # TODO: Some changges in greedy patter needed, to match big patterns first before small ones.
    #
    # Word: marmerplaatsbepaling
    # Right: mar-mer-plaats-be-pa-ling
    #
    # Word: ochtendjaskledinghangerschroefdraad
    # Wrong: och-tend-jas-kle-ding-hang-er-schroef-draad
    # Right: och-tend-jas-kle-ding-han-ger-schroef-draad
    #
    # Word: hagelslagroomboterbloemkoolstofzuigerveerpont
    # Wrong: ha-gel-slag-room-bot-er-bloem-kool-st-of-zuig-er-veer-pont
    # Right: ha-gel-slag-room-bo-ter-bloem-kool-stof-zui-ger-veer-pont

    hWords = hyphenatedWords(language) or {} # Empty dictionary if the langueage does not exist.
    hyphenated = hWords.get(word)
    if hyphenated is not None: # If exact, then stop searching.
        return hyphenated
    # In case the language support combined words, try to find matching parts.
    # TODO: Needs some adjustments for words with more than 2 parts, to take greedy large patterns
    # to check first
    if checkCombined and len(word) > 4:
        # Cecking on combined words (as in 'nl' and 'de').
        for i in range(2, len(word)-2):
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

    