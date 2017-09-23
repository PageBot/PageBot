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
#     gitview.py
#
from pagebot.contexts import HtmlContext
from pagebot.elements.views.htmlview import HtmlView

class GitView(HtmlView):
    viewId = 'Git'
    
    GIT_PATH = 'docs/'
    DEFAULT_HTML_FILE = 'index.html'
    DEFAULT_HTML_PATH = GIT_PATH + DEFAULT_HTML_FILE
    DEFAULT_CSS_PATH = GIT_PATH + 'css/pagebot.css'
    
    #   B U I L D  H T M L  /  C S S

    def build_html(self, path=None, pageSelection=None, multiPage=True):
        doc = self.doc
        sitePath = path or self.GIT_PATH
        if not sitePath.endswith('/'):
            sitePath += '/'
        b = self.c.b # Get builder of current context.
        doc.build_css(self) # Make doc build the main/overall CSS.
        for pn, pages in doc.pages.items():
            for page in pages:
                b.resetHtml()
                fileName = page.name
                if not fileName:
                    fileName = DEFAULT_HTML_FILE
                if not fileName.lower().endswith('.html'):
                    fileName += '.html'
                path = sitePath + fileName
                page.build_html(self) # Building HTML and CSS, storage in builder.
                b.writeHtml(path)
        # Write all collected CSS into one file
        b.writeCss(self.DEFAULT_CSS_PATH)

    def getUrl(self, name):
        return 'http://%s/%s' % (name, self.DEFAULT_HTML_FILE)


