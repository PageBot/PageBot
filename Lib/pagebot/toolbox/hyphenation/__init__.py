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

def hyphenate(word, language=DEFAULT_LANGUAGE):
    return (hyphenatedWords(language) or {}).get(word)

