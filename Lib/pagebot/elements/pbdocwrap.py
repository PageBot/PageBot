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
#     pbdocwrap.py
#
from pagebot.elements.element import Element
from pagebot.toolbox.color import noColor

class DocWrap(Element):
    """The DocWrap is used to create a watershed between a Document instance
    (which is not an Element by itself) and the Document that self is part of.
    This way we can avoid the mixing between rootStyles and also it allows 
    the output of documents to be cached and places on a page, independent from
    the parent page settings itself.
    """
    def __init__(self, document, docCacheType=None, pn=None, **kwargs):
        """Store document, to by used as background drawing for self.
        Note that as with any Element, child elements can be added for display.

        >>> from pagebot.document import Document
        >>> from pagebot.elements import *
        >>> doc1 = Document(name='Placed Document', w=300, h=400)
        >>> page = doc1[1]
        >>> e = Rect(parent=page, fill='red')
        >>> doc2 = Document(name='Canvas Document')
        >>> page = doc2[1]
        >>> e = DocWrap(doc1, parent=page, x=100, y=200, fill=0.5)
        >>> doc2.export('_export/ExampleDocWrap.pdf')
        """
        Element.__init__(self, **kwargs)
        assert document is not self.doc # Make sure there is not circular reference.
        self.wrappedDocument = document
        self.docCacheType = docCacheType # TODO: Currently not used.
        self.pn = pn or 1 # In case a specific page is selected.

    def _get_w(self):
        return self.wrappedDocument.block[2]
    def _set_w(self, w):
        # Ignore setting of w, entirely defined by contained self.document.block[2]
        pass
    w = property(_get_w, _set_w)
    
    def _get_h(self):
        return self.wrappedDocument.block[3]
    def _set_h(self, h):
        # Ignore setting of h, entirely defined by contained self.document.block[3]
        pass        
    h = property(_get_h, _set_h)
 
    def buildElement(self, view, p, drawElements=True, **kwargs):
        """Find the referred page of self.wrappedDocument and continue the 
        building there. Since the page does not change parent, all local styles
        and references are exactly the same, as if the wrapped document is building.
        """
        # FIXME: Hack for now, to reset outline drawing, caused by previous view drawing.
        view.context.stroke(noColor)
        view.context.fill(noColor)

        page = self.wrappedDocument[self.pn]
        page.buildElement(view, p, drawElements, **kwargs)

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
