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
        self.cssClass = self.cssClass or 'page' # Defined default CSS class for pages.
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

        >>> import os
        >>> from pagebot.contexts.htmlcontext import HtmlContext
        >>> context = HtmlContext()
        >>> from pagebot.document import Document
        >>> doc = Document(name='TestDoc', autoPages=1, context=context)
        >>> view = doc.newView('Mamp')
        >>> view.doExport = False # View flag to avoid exporting to files.
        >>> page = doc[1]
        >>> view.build()
        >>> #TODO: Get the test to work.
        >>> #os.system(u'open "%s"' % view.getUrl(doc.name))
        """
        context = view.context # Get current context and builder from this view.
        b = context.b # This is a bit more efficient than self.b once we got the context fixed.
       
        if self.info.htmlPath is not None:
            b.importHtml(self.info.htmlPath) # Add HTML content of file, if path is not None and the file exists.
        else:
            b.docType('html')
            b.html()#lang="%s" itemtype="http://schema.org/">\n' % self.css('language'))
            #
            #   H E A D
            #
            # Build the page head. There are 3 option (all not including the <head>...</head>)
            # 1 As html string (info.headHtml is defined as not None)
            # 2 As path a html file, containing the string between <head>...</head>.
            # 3 Constructed from info contect, page attributes and styles.
            #
            b.head()
            if self.info.headHtmlCode is not None:
                b.addHtml(self.info.headHtmlCode)
            elif self.info.headHtmlPath is not None:
                b.importHtml(self.info.headHtmlPath) # Add HTML content of file, if path is not None and the file exists.
            else:
                b.meta(charset=self.css('encoding'))
                # Try to find the page name, in sequence order of importance. 
                b.title_(self.info.title or self.title or self.name)
                
                # Devices
                b.meta(name='viewport', content=self.info.viewPort) # Cannot be None

                # Javascript
                if self.info.jsUrls is not None:
                    for jsUrl in self.info.jsUrls.values():
                        b.script(type="text/javascript", src=jsUrl)

                # Webfonts
                if self.info.webFontsUrl:
                    b.link(rel='stylesheet', type="text/css", href=self.info.webFontsUrl, media='all')
                
                # CSS
                if self.info.cssUrls is not None:
                    for cssUrl in self.info.cssUrls:
                        b.link(rel='stylesheet', href=cssPath, type='text/css', media='all')
                else:
                    cssPath = 'css/style.css' # Default css path
                    b.link(rel='stylesheet', href=cssPath, type='text/css', media='all')

                if self.info.cssCode is not None:
                    b.addCss(self.info.cssCode)
                if self.info.cssPath is not None:
                    b.importCss(self.info.cssPath) # Add HTML content of file, if path is not None and the file exists.

                # Icons
                if self.info.favIconUrl: # Add the icon link and let the type follow the image extension.
                    b.link(rel='icon', href=self.info.favIconUrl, type='image/%s' % self.info.favIconUrl.split('.')[-1])
                if self.info.appleTouchIconUrl: # Add the icon link and let the type follow the image extension.
                    b.link(rel='apple-touch-icon-precomposed', href=self.info.appleTouchIconUrl, type='image/%s' % self.info.appleTouchIconUrl.split('.')[-1])
                
                # Description and keywords
                if self.info.description:
                    b.meta(name='description', content=self.info.description)
                if self.info.keyWords:
                    b.meta(name='keywords', content=self.info.keyWords)
            b._head()
            #
            #   B O D Y
            #
            # Build the page body. There are 3 option (all excluding the <body>...</body>)
            # 1 As html string (self.info.bodyHtml is defined as not None)
            # 2 As path a html file, containing the string between <body>...</body>, excluding the tags
            # 3 Constructed from view parameter context, page attributes and styles.
            #
            b.body()
            if self.info.bodyHtmlCode is not None:
                b.addHtml(self.info.bodyHtmlCode)
            elif self.info.bodyHtmlPath is not None:
                b.importHtml(self.info.bodyHtmlPath) # Add HTML content of file, if path is not None and the file exists.
            else:
                b.div(cssClass=self.cssClass) # Class is standard 'page' if self.cssClass is undefined as None.
                if drawElements:
                    for e in self.elements:
                        e.build_html(view, origin)
                b._div()
            #
            #   J A V A S C R I P T
            #
            # Build the LS body. There are 3 option (all not including the <body>...</body>)
            # 1 As html string (info.headHtmlCode is defined as not None)
            # 2 As path a html file, containing the string between <head>...</head>.
            # 3 Constructed from info contect, page attributes and styles.
            #
            if self.info.jsCode is not None:
                b.addHtml(self.info.jsCode)
            if self.info.jsPath is not None:
                b.importHtml(self.info.jsPath) # Add JS content of file, if path is not None and the file exists.
            if b._jsOut:
                b.script()
                b.addHtml('\n'.join(b._jsOut))
                b._script()
            #else no default JS. To be added by the calling application.

            # Close the document
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
