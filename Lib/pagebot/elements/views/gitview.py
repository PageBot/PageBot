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
#     gitview.py
#
import os

from pagebot.elements.views.siteview import SiteView

class GitView(SiteView):
    viewId = 'Git'

    GIT_PATH = 'docs/'
    DEFAULT_HTML_FILE = 'index.html'
    DEFAULT_HTML_PATH = GIT_PATH + DEFAULT_HTML_FILE
    DEFAULT_CSS_PATH = GIT_PATH + 'css/style.css'

    #   B U I L D  H T M L  /  C S S

    def build(self, path=None, pageSelection=None, multiPage=True, **kwargs):
        """
        Default building to non-website media.
        """
        doc = self.doc 
        b = self.context.b

        if path is None:
            path = self.SITE_PATH
        if not path.endswith('/'):
            path += '/'
        if not os.path.exists(path):
            os.makedirs(path)

        # Recursively let all elements prepare for the upcoming build_html, e.g. by saving scaled images
        # into cache if that file does not already exists. Note that this is done on a page-by-page
        # level, not a preparation of all
        for pn, pages in doc.pages.items():
            for page in pages:
                hook = 'prepare_' + b.PB_ID # E.g. page.prepare_html()
                getattr(page, hook)(self) # Typically calling page.prepare_html

        # If resources defined, copy them to the export folder.
        self.copyResources(path)

        for pn, pages in doc.pages.items():
            for page in pages:
                # Building for HTML, try the hook. Otherwise call by main page.build.
                hook = 'build_' + self.context.b.PB_ID # E.g. page.build_html()
                getattr(page, hook)(self, path) # Typically calling page.build_html
                
    def getUrl(self, name):
        return 'http://%s/%s' % (name, self.DEFAULT_HTML_FILE)


