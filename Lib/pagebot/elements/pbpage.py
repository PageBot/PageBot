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
#     pbpage.py
#
import weakref
import os

from pagebot.elements.element import Element
from pagebot.elements.pbgalley import Galley
from pagebot.toolbox.units import pointOffset
from pagebot.toolbox.transformer import path2Dir, path2Url, path2FlatUrl
from pagebot.constants import ORIGIN

class Page(Element):
    """The Page container is typically the root of a tree of Element instances.
    A Document contains a set of pages.

    Because pages are built into fixed media such as PDF, PNG, animated GIF's, or
    HTML pages, a Page contains a mixture of available meta data."""

    isPage = True

    VIEW_PORT = "width=device-width, initial-scale=1.0, user-scalable=yes"
    FAVICON_PATH = 'images/favicon.ico'
    INDEX_HTML = 'index.html'
    INDEX_HTML_URL = INDEX_HTML

    GALLEY_CLASS = Galley

    def __init__(self, originTop=None, isLeft=None, isRight=None, name=None,
            htmlCode=None, htmlPath=None, headCode=None, headPath=None, 
            bodyCode=None, bodyPath=None,
            cssCode=None, cssPaths=None, cssUrls=None, jsCode=None,
            jsPaths=None, jsUrls=None, viewPort=None, favIconUrl=None,
            fileName=None, url=None, webFontUrls=None, pn=None, **kwargs):
        """Add specific parameters for a page, besides the parameters for standard Elements.

        >>> page = Page(name='MyPage')
        >>> page.w, page.h
        (100pt, 100pt)
        >>> page.size = 1111, 2222
        >>> page.size
        (1111pt, 2222pt)
        >>> page
        <Page MyPage (1111pt, 2222pt)>
        """
        Element.__init__(self, **kwargs)

        self.originTop = originTop # Set property, used by all child elements as reference.

        self.cssClass = self.cssClass or 'page' # Defined default CSS class for pages.
        # Overwrite flag for side of page. Otherwise test on document pagenumber.
        self._isLeft = isLeft
        self._isRight = isRight
        # Optional storage of page number in the page (normally this is owned
        # by the containing document). It is used if the pagnumbering of the
        # document with format (1, 0) is different from the pagnumber that
        # needs to be shown in the page.
        self.pn = pn

        #   F I L E  S T U F F

        # Used for links to home or current page url. Also used by Document.getPageTree()
        # to answer the nexted dict/list for pages, so Navigation can build a tree of
        # menu items. Url is a property to make sure that spaces are removed and all lower case.
        self.url = url or self.INDEX_HTML_URL # Property to make sure that the url is a default file.
        self.name = name # Set property. If undefined, takes the file part of self.url
        self.fileName = fileName # Set property. If undefined, takes the file part of self.url

        #   H T M L  S T U F F

        # Site stuff
        self.viewPort = viewPort or self.VIEW_PORT
        self.appleTouchIconUrl = None
        self.favIconUrl = favIconUrl or self.FAVICON_PATH

        # Optional resources that can be included for web output (HtmlContext).
        # Define string or file paths where to read content, instead of
        # constructing by the builder.  See also self.htmlCode and
        # self.htmlPath as defined for all Element classes.

        self.headCode = headCode # Optional set to string that contains the page <head>...</head>, including the tags.
        self.headPath = headPath # Set to path, if head is available in a single file, including the tags.

        self.cssCode = cssCode # Set to string, if CSS is available as single source. Exported as css file once.
        self.cssPaths = cssPaths # Set to path, if CSS is available in a single file to be included in the page.
        self.cssUrls = cssUrls # Optional CSS, if different from what is defined by the view.

        self.bodyCode = bodyCode # Optional set to string that contains the page <body>...</body>, including the tags.
        self.bodyPath = bodyPath # Set to path, if body is available in a single file, including the tags.

        self.jsCode = jsCode # Set to path, if JS is available in a single file, including the tags.
        self.jsPaths = jsPaths # Optional javascript, to be added at the end of the page, inside <body>...</body> tag.
        self.jsUrls = jsUrls # Optional Javascript Urls in <head>, if different from what is defined by the view.

        self.webFontUrls = webFontUrls # Optional set of webfont urls if different from what is in the view.

    def _get_url(self):
        return path2Url(self._url)
    def _set_url(self, path):
        """Make all lower case and remove spaces."""
        self._url = path
    url = property(_get_url, _set_url)

    def _get_flatUrl(self):
        return path2FlatUrl(self._url)
    flatUrl = property(_get_flatUrl, _set_url)

    def _get_fileName(self):
        if self._fileName is None: # If not defined, try to get it from the url
            return self.url.split('/')[-1]
        return self._fileName
    def _set_fileName(self, fileName):
        self._fileName = fileName
    fileName = property(_get_fileName, _set_fileName)

    def _get_name(self):
        if self._name is None: # If not defined, try to get it from the url/fileName
            return self.fileName
        return self._name
    def _set_name(self, name):
        self._name = name
    name = property(_get_name, _set_name)

    def _get_title(self):
        if self._title is None: # If not defined, try to get the name/fileName/url
            return self.name
        return self._title
    def _set_title(self, title):
        self._title = title
    title = property(_get_title, _set_title)

    def __repr__(self):
        """Page as string. Similar to general Element.__repr__, except showing
        the (pagenNumber, index) as it is stored in the parent document. And
        not showing (self.x, self.y), as most pages will not be part of another
        page (although it is allowed and there could be situations to do so,
        e.g. if a page is used as illustration in another page.)

        >>> from pagebot.document import Document
        >>> from pagebot.constants import A4
        >>> doc = Document(name='TestDoc', autoPages=8, size=A4)
        >>> doc[5] # Remembers original unit size.
        <Page #5 default (210mm, 297mm)>
        """
        if self.title:
            name = ' ' + self.title
        elif self.name:
            name = ' ' + self.name
        else: # No name
            name = ' Unplaced'

        if self.elements:
            elements = ' E(%d)' % len(self.elements)
        else:
            elements = ''

        pn = ''
        if self.parent: # If there is a parent, get the (pageNumber, index) tuple.
            if self._pn is not None: # Hard coded page number, then ignore document index.
                pn_index = self._pn
            else:
                pn_index = self.parent.getPageNumber(self)
            if pn_index is not None:
                if pn_index[1]: # Index > 1, then show.
                    pn = ' #%d:%d' % pn_index
                else:
                    pn = ' #%d' % pn_index[0]

        return '<%s%s%s (%s, %s)%s>' % (self.__class__.__name__, pn, name, self.w, self.h, elements)

    def _get_originTop(self):
        """Answers the style flag if all point y values should measure top-down
        (typographic page orientation), instead of bottom-up (mathematical
        orientation). For Y-axis only. The axes in X and Z directions are
        fixed. The value is stored on page level, so there is no origin top/down
        switching possible inside the element tree of a page.
        Note that by changing, the position of existing glyphs does NOT change,
        so their (x,y) position changes (unless referred to by side positions
        such as e.top and e.center, etc.).

        Position of origin. DrawBot has y on bottom-left. In PageBot it is
        optional. Default is bottom-left. Note that the direcion of display is
        always upwards. This means that the position of text and elements
        goes downward from the top, they are not flipped vertical. It is up
        to the caller to make sure there is enough space for elements to show
        themselves on top of a given position. originTop often goes with
        """
        return self._originTop
    def _set_originTop(self, flag):
        self._originTop = bool(flag) # Value is stored in the page.
    originTop = property(_get_originTop, _set_originTop)

    def _get_isLeft(self):
        """Answers if this is a left page (even pagenumber), unless the
        self._isLeft is overwritten by a boolean, other than None. Note
        that pages can be both left or right.

        >>> from pagebot.document import Document
        >>> doc = Document(name='TestDoc', autoPages=8)
        >>> page = doc[5]
        >>> page.isLeft
        False
        >>> page.isLeft = True
        >>> page.isLeft
        True
        >>> page.isLeft = None # Reset to automatic behavior by setting as None
        >>> page.isLeft
        False
        """
        if self._isLeft is not None:
            return self._isLeft
        if self.parent is not None:
            return self.parent.getPageNumber(self)[0] % 2 == 0
        return None

    def _set_isLeft(self, flag):
        self._isLeft = flag

    isLeft = property(_get_isLeft, _set_isLeft)

    def _get_isRight(self):
        """Answers if this is a right page, if that info is stored. Note that
        pages can be neither left or right. Otherwise, the only one who can
        know that is the document.

        >>> from pagebot.document import Document
        >>> doc = Document(name='TestDoc', autoPages=8)
        >>> page = doc[5]
        >>> page.isLeft # Uneven is automatic right page.
        False
        >>> page.isLeft = True # Unless forced to be left.
        >>> page.isLeft
        True
        >>> page.isLeft = None # Reset to automatic behavior by setting as None
        >>> page.isLeft
        False
        """
        if self._isRight is not None: # Overwritted by external call.
            return self._isRight
        if self.doc is not None:
            return self.parent.getPageNumber(self)[0] % 2 == 1

        return None

    def _set_isRight(self, flag):
        self._isRight = flag

    isRight = property(_get_isRight, _set_isRight)

    def _get_next(self):
        """Answers the page with the next page number the document, relative to
        self. Create a new page if self is the last page in the self.parent
        document. Answer None if the self page has no parent.

        >>> from pagebot.document import Document
        >>> doc = Document(name='TestDoc', autoPages=8)
        >>> page = doc[5]
        >>> page.next.pn # Skip any sub-pages with the same page number.
        (6, 0)
        >>> page.next.next.pn
        (7, 0)
        >>> page.next.prev is page
        True
        """
        if self.parent is None:
            return None

        return self.parent.nextPage(self)

    next = property(_get_next)

    def _get_prev(self):
        u"""Answers the previous page in the document, relative to self. Answer
        None if self is the first page.

        >>> from pagebot.document import Document
        >>> doc = Document(name='TestDoc', autoPages=8)
        >>> page = doc[5]
        >>> page.prev.pn # Skip any sub-pages with the same page number.
        (4, 0)
        >>> page.prev.prev.pn
        (3, 0)
        >>> page.prev.next is page
        True
        """
        if self.parent is None:
            return None
        return self.parent.prevPage(self)

    prev = property(_get_prev)

    def _get_pn(self):
        """Answers the page number by which self is stored in the parent
        document. To move or remove pages, use Document.movePage() or
        Document.removePage() In case the self._pn is set, the page numbering
        is hard-coded, independent of the pages in the containing document.

        >>> from pagebot.document import Document
        >>> doc = Document(name='TestDoc', autoPages=8)
        >>> sorted(doc.pages.keys())
        [1, 2, 3, 4, 5, 6, 7, 8]
        >>> page = doc[5]
        >>> page.pn
        (5, 0)
        >>> page.pn = 320 # Overwrites the document paging
        >>> page.pn
        (320, 0)
        >>> page.pn = None # Reset document paging
        >>> page.pn
        (5, 0)
        """
        if self._pn is not None:
            return self._pn
        if self.parent is None:
            return None # Not placed directly in a document. No page number known.
        return self.parent.getPageNumber(self)

    def _set_pn(self, pn):
        """Set the optional page numbere, overwriting queries into the
        containing document."""
        if pn is not None and not isinstance(pn, (list, tuple)):
            pn = pn, 0
        self._pn = pn

    pn = pageNumber = property(_get_pn, _set_pn)

    #   E L E M E N T S

    def getGalley(self, name=None):
        """Answers the default galley element of a page. This is used in case
        pages need to be made with content (e.g. to accommodate overflow)
        without a main sequence of text boxes in stalled or without an applied
        template that contains them. Usage of the default page galley is
        mostly for booting a document, without the final layout defined.

        The reason to add this as function / property in the page is for
        convenient access in MarkDown content files.
        """
        if name is None:
            name = self.INDEX_HTML
        galley = self.select(name)
        if galley is None:
            galley = Galley(name=name, parent=self, xy=self.xy, size=self.pw, nextElement=name)
        return galley

    def _get_galley(self):
        return self.getGalley()
    galley = property(_get_galley)

    #   C O M P O S I T I O N  S U P P O R T

    def compose(self, doc, publication):
        """Recusively compose Page and add it to doc. Note that this will alter
        the self.parent to doc. The recursively pass the composing on to the
        page elements, which at that time can use the full document style
        settings by e.css(...)."""
        doc.appendPage(self)
        for e in self.elements:
            e.compose(doc, publication)

    #   D R A W B O T  &  F L A T  S U P P O R T

    def build(self, view, origin=ORIGIN, drawElements=True, **kwargs):
        """Draws all elements of this page in DrawBot. Note that this method is
        only used in case pages are drawn as element on another page. In normal
        usage, pages get drawn by PageView.build"""
        p = pointOffset(self.origin, origin) # Ignoe z-axis for now.

        view.drawPageMetaInfo(self, p, background=True)

        # If there are child elements, draw them over the text.
        if drawElements:
            self.buildChildElements(view, p, **kwargs) # Build child elements, depending in context build implementations.

        # Draw addition page info, such as crop-mark, registration crosses,
        # etc. if parameters are set.
        view.drawPageMetaInfo(self, p, background=False)

        # Check if we are in scaled mode. Then restore.
        #self._restoreScale()

    #   H T M L  /  C S S  S U P P O R T

    def build_html(self, view, path):
        """Builds the HTML/CSS code through WebBuilder (or equivalent) that is
        the closest representation of self. If there are any child elements,
        then also included their code, using the level recursive indent.

        Single page site, exporting to html source, with CSS inside.
        >>> import os
        >>> from pagebot.document import Document
        >>> doc = Document(name='SinglePageSite', viewId='Site')
        >>> page = doc[1]
        >>> page.title = 'Home'
        >>> page.cssCode = 'body {background-color:black}'
        >>> exportPath = '_export/Home' # No extension for site folder if exporting to a website
        >>> #doc.export(exportPath)
        >>> #result = os.system('open %s/index.html' % exportPath)
        """
        context = view.context # Get current context and builder from this view.
        b = context.b # This is a bit more efficient than self.b once we got the context fixed.
        b.clearHtml()
        #b.clearCss()

        self.build_scss(view)

        if self.htmlCode: # In case the full HTML is here, then just output it.
            b.addHtml(self.htmlCode) # This is mostly used for debug and new templates.
        elif self.htmlPaths is not None:
            for htmlPath in self.htmlPaths:
                b.importHtml(htmlPath) # Add HTML content of file, if path is not None and the file exists.
        else:
            b.docType('html')
            b.html()#lang="%s" itemtype="http://schema.org/">\n' % self.css('language'))
            #
            #   H E A D
            #
            # Build the page head. There are 3 option (all including the <head>...</head>)
            # 1 As html string (info.headHtml is defined as not None)
            # 2 As path a html file, containing the string between <head>...</head>.
            # 3 Constructed from info contect, page attributes and styles.
            #
            if self.headCode is not None:
                b.addHtml(self.headCode)
            elif self.headPath is not None:
                b.importHtml(self.headPath) # Add HTML content of file, if path is not None and the file exists.
            else:
                b.head()
                
                # Add Google Analytics if accounts numbers are defined.
                if view.googleAdsAccount is not None and view.googleAnalyticsId is not None:
                    gaScript_XXX = """<!-- Global Site Tag (gtag.js) - Google Analytics -->
                        <script async src="https://www.googletagmanager.com/gtag/js?id=%(googleAnalyticsId)s"></script>
                        <script>
                          window.dataLayer = window.dataLayer || [];
                          function gtag(){dataLayer.push(arguments);}
                          gtag('js', new Date());

                          gtag('config', '%(googleAnalyticsId)s');
                        </script>
                    """ % dict(googleAnalyticsId=view.googleAnalyticsId)
                    gaScript = """
                    <script>
                    (function(i,s,o,g,r,a,m){
                      i['GoogleAnalyticsObject']=r;
                      i[r]=i[r]||function(){(i[r].q=i[r].q||[]).push(arguments)},
                      i[r].l=1*new Date();
                      a=s.createElement(o),m=s.getElementsByTagName(o)[0];
                      a.async=1;
                      a.src=g;
                      m.parentNode.insertBefore(a,m)
                    })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

                    ga('create', '%(googleAnalyticsId)s', 'auto');
                    ga('send', 'pageview');
                    </script>
                    """ % dict(googleAnalyticsId=view.googleAnalyticsId)
                    b.addHtml(gaScript)

                b.meta(charset=self.css('encoding')) # Default utf-8
                # Try to find the page name, in sequence order of importance.
                b.title_(self.title or self.name or self.url.split('/')[-1])

                b.meta(httpequiv='X-UA-Compatible', content='IE=edge,chrome=1')

                # Devices
                if self.viewPort is not None: # Not supposed to be None. Check anyway
                    b.comment('Mobile viewport')
                    b.meta(name='viewport', content=self.viewPort)

                # View and pages can both implements Webfonts urls
                for webFontUrls in (view.webFontUrls, self.webFontUrls):
                    if webFontUrls is not None:
                        for webFontUrl in webFontUrls:
                            b.link(rel='stylesheet', type="text/css", href=webFontUrl, media='all')

                # If there is cumulated CSS in the builder, e.g. by individual elements for this page
                # only, then add that directly inside the page
                if b.hasCss():
                    b.style()
                    b.addHtml(b.getCss())
                    b._style()

                # View and pages can both implements CSS paths
                for cssUrls in (view.cssUrls, self.cssUrls):
                    if cssUrls is not None:
                        for cssUrl in cssUrls:
                            b.link(rel='stylesheet', href=cssUrl, type='text/css', media='all')

                # Use one of both of these options in case CSS needs to be copied into the page.
                for cssCode in (view.cssCode, self.cssCode):
                    if cssCode is not None:
                        # Add the code directly into the page if it is not None
                        b.style()
                        b.addHtml(cssCode)
                        b._style()

                # Use one or both of these options in case CSS is needs to be copied from files into the page.
                for cssPaths in (view.cssPaths, self.cssPaths):
                    if self.cssPaths:
                        b.style()
                        for cssPath in cssPaths:
                            # Include CSS content of file, if path is not None and the file exists.
                            b.importHtml(cssPath)
                        b._style()

                # Icons
                if self.favIconUrl: # Add the icon link and let the type follow the image extension.
                    b.link(rel='icon', href=self.favIconUrl, type='image/%s' % self.favIconUrl.split('.')[-1])
                if self.appleTouchIconUrl: # Add the icon link and let the type follow the image extension.
                    b.link(rel='apple-touch-icon-precomposed', href=self.appleTouchIconUrl, type='image/%s' % self.appleTouchIconUrl.split('.')[-1])

                # Description and keywords
                if self.description:
                    b.meta(name='description', content=self.description)
                if self.keyWords:
                    b.meta(name='keywords', content=self.keyWords)
                b._head()
            #
            #   B O D Y
            #
            # Build the page body. There are 3 option (all excluding the <body>...</body>)
            # 1 As html string (self.bodyCode is defined as not None)
            # 2 As path to a html file, containing the string between <body>...</body>, including the tags
            # 3 Constructed from view parameter context, page attributes and styles.
            #
            if self.bodyCode is not None:
                b.addHtml(self.bodyCode)
            elif self.bodyPath is not None:
                b.importHtml(self.bodyPath) # Add HTML content of file, if path is not None and the file exists.
            else:
                b.body()
                for e in self.elements:
                    e.build_html(view, path)
                #
                #   J A V A S C R I P T
                #
                # Build the JS body. There are 4 option (all not including the <script>...</script>)
                # 1 As path a html file, containing the string between <script>...</script>, including the tags.
                # 2 Constructed from info context, page attributes and styles.
                # 3 As cumulated inside builders (from b.getJs())
                # 4 As html/javascript string (view.jsCode and/or self.jsCode are defined as not None)
                #
                for jsUrls in (view.jsUrls, self.jsUrls):
                    if jsUrls is not None:
                        for jsUrl in jsUrls:
                            b.script(type="text/javascript", src=jsUrl)

                for jsPaths in (view.jsPaths, self.jsPaths):
                    if jsPaths:
                        for jsPath in jsPaths:
                            b.script(type="text/javascript")
                            b.addHtml(jsPath)
                            b._script()

                if b.hasJs():
                    b.script(type="text/javascript")
                    b.addHtml(b.getJs())
                    b._script()

                for jsCode in (view.jsCode, self.jsCode):
                    if jsCode is not None:
                        b.script(type="text/javascript")
                        b.addHtml(jsCode)
                        b._script()

                # Close the page body
                b._body()
            b._html()

        if view.doExport: # View flag to avoid writing, in case of testing.
            # Construct the file name for this page and save the file.
            url = self.url.lower()  
            if not url.endswith('.html'):
                url += '.html'

            # Make sure that the root path folder of the site is there
            if not path.endswith('/'):
                path += '/'
            # Decide to save as folders (in which care relative image/CSS/JS paths
            # also need to be made relative.
            if not view.saveUrlAsDirectory:
                url = url.replace('/', '-')
            filePath = path + url
            dirPath = path2Dir(filePath)
            # Then create the folders that this page needs.
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)
            b.writeHtml(filePath)

class Template(Page):

    def __repr__(self):
        return '<Template>'

    def _get_parent(self):
        """Answers the parent of the element, if it exists, by weakref
        reference. Answer None of there is not parent defined or if the parent
        not longer exists."""
        if self._parent is not None:
            return self._parent()
        return None

    def _set_parent(self, parent):
        """Set the parent of the template. Don't call self.appendParent here,
        as we don't want the parent to add self to the page/element list. Just
        a simple reference, to connect to styles, etc."""
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
