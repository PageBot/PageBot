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
#     xmlreader.py
#
#     Read XML files from path or url and answer the etree.
#
import xml.etree.ElementTree as ET

def readXML(path, xPath=None):
    """Read the XML from path and answer the compiled etree.

    >>> from pagebot.filepaths import getResourcesPath
    >>> resourcesPath = getResourcesPath()
    >>> testSvg = resourcesPath + '/templates/test.svg'
    >>> root = readHTML(testSvg, xPath=None)
    >>> #root
    """
    fileExtension = path.split('.')[-1].lower()
    assert fileExtension.lower() in ('xml', 'xsl', 'html', 'svg', 'ufo')
    tree = ET.parse(path)
    root = tree.getroot() # Get the root element of the tree.

    # If XSL filtering is defined, they get the filtered nodes.
    if xPath is not None:
        return root.findall(xPath)
    return root

def readHTML(path, xPath=None):
    """Read the HTML body tag from path and answer the compiled etree.


    >>> from pagebot.filepaths import getResourcesPath
    >>> resourcesPath = getResourcesPath()
    >>> testHtml = resourcesPath + '/templates/test.html'
    >>> body = readHTML(testHtml)[0]
    >>> body.tag
    'body'
    >>> len(list(body))
    2
    """
    return readXML(path, xPath='body')

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
