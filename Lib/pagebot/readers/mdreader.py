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
#     mdreader.py
#
#     Read markdown files from path or url and answer the etree.
#
import codecs
from xmlreader import readXML

try:
    import markdown
    from markdown.extensions.nl2br import Nl2BrExtension
    from pagebot.contributions.markdown.literature import LiteratureExtension
    from pagebot.contributions.markdown.footnotes import FootnoteExtension
except ImportError:
    print('Typesetter: Install Python markdown from https://pypi.python.org/pypi/Markdown')
    markdown = None

def markDown2XMLFile(path):
    u"""If fileName is pointing to a non-XML file, then try to convert. This needs to be
    extended in the future e.g. to support Word documents or other text resources.
    If the document is already an XML document, then ignore."""
    fileExtension = path.split('.')[-1].lower()
    assert fileExtension.lower() == 'md'
    # If we have MarkDown content, convert to XML (XHTML)
    f = codecs.open(path, mode="r", encoding="utf-8")
    mdText = f.read()
    f.close()
    mdExtensions = [FootnoteExtension(), LiteratureExtension(), Nl2BrExtension()]
    xml = u'<?xml version="1.0" encoding="UTF-8"?>\n<document>%s</document>' % markdown.markdown(mdText, extensions=mdExtensions)
    xml = xml.replace('&nbsp;', ' ')

    xmlPath = path + '.xml'
    print(xmlPath)
    f = codecs.open(xmlPath, mode="w", encoding="utf-8")
    f.write(xml)
    f.close()
    return xmlPath # Return altered fileName if converted. Otherwise return original fileName

def readMD(path):
    u"""Read the markdown from path and answer the compiled etree."""
    xmlPath = markDown2XMLFile(path)
    return readXML(xmlPath)

