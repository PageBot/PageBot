#!/usr/bin/env python
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

    def build(self, path=None, pageSelection=None, multiPage=True):
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
            assert path and not os.path.exists(path), '[MampView.build] Export site path "%s" exists: delete manually' % (path)
            if not path.endswith('/'):
                path += '/'

        for pn, pages in self.doc.pages.items():
            for page in pages:
                # Building for HTML, try the hook. Otherwise call by main page.build.
                hook = 'build_' + self.context.b.PB_ID # E.g. page.build_html()
                getattr(page, hook)(self, path) # Typically calling page.build_html

        # Write all collected SCSS vatiables into one file
        self.context.b.writeScss(self.SCSS_VARIABLES_PATH)
        # Compile SCSS to CSS
        #self.context.b.compileScss(self.SCSS_PATH, self.SCSS_CSS_PATH)

        # If resources defined, copy them to the export folder.
        self.copyResources(path)


    def getUrl(self, name):
        """Answer the local URL for Mamp Pro to find the copied website."""
        return self.LOCAL_HOST_URL % (name, self.DEFAULT_HTML_FILE)


if __name__ == "__main__":
    import sys
    import doctest
    sys.exit(doctest.testmod()[0])
