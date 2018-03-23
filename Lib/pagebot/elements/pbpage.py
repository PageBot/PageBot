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
#     page.py
#
import weakref
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset
from pagebot.style import ORIGIN

class Page(Element):

    isPage = True

    def __init__(self, leftPage=None, rightPage=None, **kwargs):  
        u"""Add specific parameters for a page, besides the parameters for standard Elements.

        >>> page = Page()
        >>> page.w, page.h
        (100, 100)
        >>> page.w = 1111
        >>> page.w, page.h
        (1111, 100)
        """
        Element.__init__(self,  **kwargs)
        self.class_ = self.class_ or 'page' # Defined default CSS class for pages.
        self._isLeft = self._isRight = None # Undefined, lef self.doc decide.

    def _get_isLeft(self):
        u"""Answer the boolean flag if this is a left page, if that info is stored. 
        Note that pages can be neither left or right.
        Otherwise, the only one who can know that is the document.

        >>> from pagebot.document import Document
        >>> doc = Document(name='TestDoc', autoPages=8)
        >>> page = doc[5]
        >>> page.isLeft
        False
        >>> page.isLeft = True
        >>> page.isLeft
        True
        """
        if self._isLeft is not None:
            return self._isLeft   
        if self.doc is not None:
            return self.doc.isLeftPage(self) # If undefined, query parent document to decide.
        return None
    def _set_isLeft(self, flag):
        self._isLeft = flag
    isLeft = property(_get_isLeft, _set_isLeft)

    def _get_isRight(self):
        u"""Answer the boolean flag if this is a right page, if that info is stored. 
        Note that pages can be neither left or right.
        Otherwise, the only one who can know that is the document.

        >>> from pagebot.document import Document
        >>> doc = Document(name='TestDoc', autoPages=8)
        >>> page = doc[5]
        >>> page.isLeft
        False
        >>> page.isLeft = True
        >>> page.isLeft
        True
        """
        if self._isLeft is not None:
            return self._isLeft   
        if self.doc is not None:
            return self.doc.isLeftPage(self) # If undefined, query parent document to decide.
        return None
    def _set_isRight(self, flag):
        self._isRight = flag
    isRight = property(_get_isRight, _set_isRight)

    #   D R A W B O T  & F L A T  S U P P O R T

    def build(self, view, origin=ORIGIN, drawElements=True):
        u"""Draw all elements of this page in DrawBot."""
        p = pointOffset(self.oPoint, origin) # Ignoe z-axis for now.
        # If there are child elements, draw them over the text.
        if drawElements:
            self.buildChildElements(view, p) # Build child elements, depending in context build implementations.
        # Draw addition page info, such as crop-mark, registration crosses, etc. if parameters are set.
        view.drawPageMetaInfo(self, origin)
        # Check if we are in scaled mode. Then restore.
        #self._restoreScale()

    #   H T M L  /  C S S  S U P P O R T

    def build_html(self, view, origin=None, drawElements=True):
        u"""Build the HTML/CSS code through WebBuilder (or equivalent) that is the closest representation 
        of self. If there are any child elements, then also included their code, using the
        level recursive indent.

        >>> from pagebot.document import Document
        >>> doc = Document(name='TestDoc', autoPages=4)
        >>> view = doc.newView('Mamp')
        >>> page = doc[1]
        >>> view.build()

        """
        context = self.context # Get current context and builder.
        b = context.b # This is a bit more efficient than self.b once we got the context fixed.
       
        self.build_css(view)
        info = self.info # Contains flags and parameterss for Builder "b"
        if info.htmlPath is not None:
            b.importHtml(info.htmlPath) # Add HTML content of file, if path is not None and the file exists.
        else:
            b.docType('html')
            b.html()#lang="%s" itemtype="http://schema.org/">\n' % self.css('language'))
            if info.headPath is not None:
                b.importHtml(info.headPath) # Add HTML content of file, if path is not None and the file exists.
            else:
                b.head()
                b.meta(charset=self.css('encoding'))
                # Try to find the page name, in sequence order of importance. Note that self.info gets copied from
                # templates (supplying a generic title or name), which can be overwritted by the direct self.title
                # and self.name of the the page element.
                b.title_(self.title or self.name or info.title or info.name)
                
                # Devices
                b.meta(name='viewport', content=info.viewPort) # Cannot be None
                # Javascript
                if info.jQueryUrl:
                    b.script(type="text/javascript", src=info.jQueryUrl)
                if info.jQueryUrlSecure:
                    b.script(type="text/javascript", src=info.jQueryUrlSecure)
                if info.mediaQueriesUrl: # Enables media queries in some unsupported browsers-->
                    b.script(type="text/javascript", src=info.mediaQueriesUrl)

                # CSS
                if info.webFontsUrl:
                    b.link(rel='stylesheet', type="text/css", href=info.webFontsUrl, media='all')
                if info.cssPath is not None:
                    cssPath = 'css/' + info.cssPath.split('/')[-1]
                else:
                    cssPath = 'css/pagebot.css'
                b.link(rel='stylesheet', href=cssPath, type='text/css', media='all')

                # Icons
                if info.favIconUrl: # Add the icon link and let the type follow the image extension.
                    b.link(rel='icon', href=info.favIconUrl, type='image/%s' % info.favIconUrl.split('.')[-1])
                if info.appleTouchIconUrl: # Add the icon link and let the type follow the image extension.
                    b.link(rel='apple-touch-icon-precomposed', href=info.appleTouchIconUrl, type='image/%s' % info.appleTouchIconUrl.split('.')[-1])
                
                # Description and keywords
                if info.description:
                    b.meta(name='description', content=info.description)
                if info.keyWords:
                    b.meta(name='keywords', content=info.keyWords)
                b._head()

            if info.bodyPath is not None:
                b.importHtml(info.bodyPath) # Add HTML content of file, if path is not None and the file exists.
            else:
                b.body()
                b.div(class_=self.class_) # Class is standard 'page' if self.class_ is undefined as None.
                if drawElements:
                    for e in self.elements:
                        e.build_html(view, origin)
                b._div()
                b._body()
            b._html()

class Template(Page):

    def _get_parent(self):
        u"""Answer the parent of the element, if it exists, by weakref reference. Answer None of there
        is not parent defined or if the parent not longer exists."""
        if self._parent is not None:
            return self._parent()
        return None
    def _set_parent(self, parent):
        u"""Set the parent of the template. Don't call self.appendParent here, as we don't want the 
        parent to add self to the page/element list. Just a simple reference, to connect to styles, etc."""
        if parent is not None:
            parent = weakref.ref(parent)
        self._parent = parent
    parent = property(_get_parent, _set_parent)

 
    def draw(self, origin, view):
        raise ValueError('Templates cannot draw themselves in a view. Apply the template to a page first.')


if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
