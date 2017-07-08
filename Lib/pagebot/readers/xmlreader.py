# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     xmlreader.py
#
#     Read XML files from path or url and answer the etree.
#
import codecs
import xml.etree.ElementTree as ET

def readXMLFile(path, xPath=None):
    u"""Read the XML from path and answer the compiled etree."""
    fileExtension = path.split('.')[-1].lower()
    assert fileExtension.lower() in ('xml', 'xsl', 'html')
    tree = ET.parse(path)
    root = tree.getroot() # Get the root element of the tree.
    # If there is XSL filtering defined, they get the filtered nodes.
    if xPath is not None:
        return root.findall(xPath)
    return root

def readHTMLFile(path, xPath=None):
    u"""Read the HTML body tag from path and answer the compiled etree."""
    return readXMLFile(path, xPath='body')