#!/usr/bin/env python
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
#     xmlreader.py
#
#     Read XML files from path or url and answer the etree.
#
import xml.etree.ElementTree as ET

def readXML(path, xPath=None):
    """Read the XML from path and answer the compiled etree."""
    fileExtension = path.split('.')[-1].lower()
    assert fileExtension.lower() in ('xml', 'xsl', 'html')
    tree = ET.parse(path)
    root = tree.getroot() # Get the root element of the tree.
    # If there is XSL filtering defined, they get the filtered nodes.
    if xPath is not None:
        return root.findall(xPath)
    return root

def readHTML(path, xPath=None):
    """Read the HTML body tag from path and answer the compiled etree."""
    return readXML(path, xPath='body')
