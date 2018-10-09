#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------

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
#     article.py
#
import os
from pagebot.typesetter import Typesetter

class Article:
    """An Article instance is the abstract binder between content (e.g. as processed by
    Typesetter, and formatted pages in a Document (required), reflecting the capabilities 
    of a given context and a given view (e.g. HTML/CSS output or PDF documents).

    It is possible that multiple Article instance refer to the same document, e.g. 
    to create chapters/articles in a range of pages. 

    Articles have no knowledge about style, sizes, etc. Those are supposed to be defined
    in the document. Instead, Articles can query the document about it, if information
    is necessary to guess the volume of a text, characteristics of installed templates, etc.

    The aim of the Article class is to implement an abstract level of content-layout
    relations. The artDirection string is a composition description (matching on keywords), 
    defining the layout and behavior of the content in the pages of the article.

    The artdirection language tags will grow over time to include  more functions.

    """

    def __init__(self, doc, artDirection, path=None, mdText=None, startPage=1, name=None, **kwargs):
        u"""Initialize the Article instance, using the initialized Document instance.

        >>> from pagebot.document import Document
        >>> from pagebot.constants import A4
        >>> doc = Document(size=A4)
        >>> ad = 'First page has a large headline and one column text. If text overfill, continue on the second page in 2 full height columns.'
        >>> md = '''# This is a head\\n## This is a subhead\\nThis is plain text.'''
        >>> a = Article(doc, ad, mdText=md)
        >>> a.typeset()

        """
        self.doc = doc # Reuired Document instance. Assummed to be initialized with size and styles.
        self.artDirection = artDirection
        self.path = path # Optional path to markdown file, if there is content there.
        self.mdText = mdText # Optional markdown string.
        self.name = name or 'Untitled'
        self.startPage = startPage

    def typeset(self): 
        u"""Take the composition descriptor of the Article and apply it to the document,
        by interpreting key words in the "free language" design talk and finding the 
        related functions to call.

        """
        if self.mdText:
            t = Typesetter(self.doc.context)
            tmpPath = '/tmp/PageBot-Article.xml' 
            path = t.markDown2XmlFile(tmpPath, self.mdText)
            galley = t.typesetFile(path)
            os.remove(tmpPath)

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
