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
#     rereader.py
#
#     Read text files, answer result of applied re-pattern.
#
import codecs

def readRE(path, pattern):
    u"""If fileName is pointing to a non-XML file, then try to read and apply the pattern on the content.
    Answer the result of the pattern match."""
    f = codecs.open(path, mode="r", encoding="utf-8")
    text = f.read()
    f.close()
    return pattern.findall(text)
