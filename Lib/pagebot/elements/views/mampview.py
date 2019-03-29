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
#     mampview.py
#
#     The MampView generates the website from the current document, and then copies
#     the files (including images, CSS, JS, etc.) to the getMampPath()+'/htdocs'
#     folder. Running local Mamp server application then does test the website.
#
import os
import shutil

from pagebot import getMampPath
from pagebot.elements.views.siteview import SiteView

class MampView(SiteView):

    viewId = 'Mamp'

    # If the MAMP server application not installed, a browser is opened on the MAMP website to download it.
    # There is a free demo version can be installed.
    MAMP_SHOP_URL = 'https://www.mamp.info/en/'
    LOCAL_HOST_URL = 'http://localhost:8888/%s/%s'
    SITE_ROOT_PATH = getMampPath()

    DEFAULT_HTML_FILE = 'index.html'
    DEFAULT_HTML_PATH = SITE_ROOT_PATH + DEFAULT_HTML_FILE
    SCSS_CSS_PATH = SITE_ROOT_PATH + 'css/style.scss.css'
    SCSS_PATH = SITE_ROOT_PATH + 'css/style.scss'
    SCSS_VARIABLES_PATH = SITE_ROOT_PATH + 'css/variables.scss'

    #   B U I L D  H T M L  /  C S S

    def build(self, path=None, pageSelection=None, multiPage=True, **kwargs):
        """

        >>> from pagebot.contributions.filibuster.blurb import Blurb
        >>> article = Blurb().getBlurb('da_text') # Answer random text of design article
        >>> from pagebot.toolbox.color import color
        >>> from pagebot.elements import newTextBox
        >>> from pagebot.document import Document
        >>> siteName = 'TestDoc'
        >>> sitePath = '_export/' + siteName
        >>> doc = Document(name=siteName, w=300, h=400, padding=(30, 40, 50, 60), viewId='Mamp')
        >>> view = doc.view
        """
        doInit = True

        rootPath = getMampPath() # Get the root path in this context where Mamp stores files.
        siteName = (self.doc.name or self.doc.title or 'UntitledSite').replace(' ','_') # Make safe site name

        if path is None:
            path = rootPath + siteName + '/'
            if os.path.exists(path): # In case of using default path, it's safe to delete.
                if self.verbose:
                    print('[MampView.build] Deleting %s' % path)
                shutil.rmtree(path)
        else: # Make sure it is not there. Remove manually otherwise.
            assert path and not os.path.exists(path), '[MampView.build] Export site path "%s" exists. For safety, delete manually' % (path)
            if not path.endswith('/'):
                path += '/'

        b = self.context.b
        pageItems = self.doc.pages.items()

        # Recursively let all elements prepare for the upcoming build_html, e.g. by saving scaled images
        # into cache if that file does not already exists. Note that this is done on a page-by-page
        # level, not a preparation of all
        for pn, pages in pageItems:
            for page in pages:
                hook = 'prepare_' + b.PB_ID # E.g. page.prepare_html()
                getattr(page, hook)(self) # Typically calling page.prepare_html. Pass self as view.

        for pn, pages in pageItems:
            for page in pages:
                b.clearJs()
                # Building for HTML, try the hook. Otherwise call by main page.build.
                hook = 'build_' + b.PB_ID # E.g. page.build_html()
                getattr(page, hook)(self, path) # Typically calling page.build_html. Pass self as view

        # Deprecated
        # TODO: Change this, so it will recognize the type of css file, and then decide on conversion
        # TODO: That also applies for th cssPy % theme.mood conversion.
        #if self.useXXXXScss:
        #    # Write all collected SCSS vatiables into one file
        #    if os.path.exists(self.SCSS_PATH):
        #        # Write all collected SCSS variables into one file
        #        b.writeScss(self.SCSS_VARIABLES_PATH)
        #        # Compile SCSS to CSS if it exists.
        #        b.compileScss(self.SCSS_PATH)

        # If resources defined, copy them to the export folder.
        self.copyResources(path)


    def getUrl(self, name):
        """Answers the local URL for Mamp Pro to find the copied website."""
        return self.LOCAL_HOST_URL % (name, self.DEFAULT_HTML_FILE)


if __name__ == "__main__":
    import sys
    import doctest
    sys.exit(doctest.testmod()[0])
