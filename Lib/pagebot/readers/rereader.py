#!/usr/bin/env python3
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
    """If fileName is pointing to a non-XML file, then try to read and apply
    the pattern on the content. Answer the result of the pattern match.

    >>> from pagebot.filepaths import getResourcesPath
    >>> resourcesPath = getResourcesPath()
    >>> testHtml = resourcesPath + '/templates/test.html'
    >>> testString = '<html><body><p>test paragraph.</p></body></html>'
    >>> import re
    >>> reNoTags = re.compile(r'<[^>]*|([^<>]*)')
    >>> result = readRE(testHtml, reNoTags)
    """
    f = codecs.open(path, mode="r", encoding="utf-8")
    text = f.read()
    f.close()
    return pattern.findall(text)

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
