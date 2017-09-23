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
import codecs

from pagebot.contexts import Context as C
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset

class Page(Element):

    isPage = True

    def __init__(self, leftPage=None, rightPage=None, **kwargs):  
        u"""Add specific parameters for a page, besides the parameters for standard Elements.
        """
        Element.__init__(self,  **kwargs)
        self.leftPage = leftPage # Force left/right side of a page, independen of document odd/even.
        self.rightPage = rightPage 
        self.class_ = self.class_ or 'page' # Defined default CSS class for pages.

    def isLeftPage(self):
        u"""Answer the boolean flag if this is a left page. The only one who can know that is the document."""
        if self.leftPage is None:
            return self.doc.isLeftPage(self) # If undefined, query parent document to decide.
        return self.leftPage   

    def isRightPage(self):
        u"""Answer the boolean flag if this is a right page. The only one who can know that is the document."""
        if self.rightPage is None:
            return self.doc.isRightPage(self)
        return self.rightPage 

    def draw(self, origin, view):
        u"""Draw all elements this page."""
        p = pointOffset(self.oPoint, origin) # Ignoe z-axis for now.
        # If there are child elements, draw them over the text.
        self._drawElements(p, view)
        # Draw addition page info, such as crop-mark, registration crosses, etc. if parameters are set.
        view.drawPageMetaInfo(self, origin)
        # Check if we are in scaled mode. Then restore.
        #self._restoreScale()

    def build(self, view):
        u"""Build the HTML/CSS code through WebBuilder (or equivalent) that is the closest representation of self. 
        If there are any child elements, then also included their code, using the
        level recursive indent."""
        b = C.b
        self.build_css(view)
        info = self.info # Contains flags and parameter to Builder "b"
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
                b.div(class_=self.class_) # Us standard 'page' if self.class_ is undefined as None.
                for e in self.elements:
                    e.build(view, b)
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