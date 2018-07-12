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
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     mampview.py
#
import os
import shutil

from pagebot.contexts.platform import getMampPath
from pagebot.elements.views.siteview import SiteView
from pagebot.style import ORIGIN


class MampView(SiteView):
    
    viewId = 'Mamp'

    # If the MAMP server application not installed, a browser is opened on the MAMP website to download it.
    # There is a free demo version can be installed.
    MAMP_SHOP_URL = 'https://www.mamp.info/en/' 
    LOCAL_HOST_URL = 'http://localhost:8888/%s/%s'
    SITE_ROOT_PATH = getMampPath()

    #   B U I L D  H T M L  /  C S S

    def build(self, path=None, pageSelection=None, multiPage=True):
        """

        >>> from pagebot.contributions.filibuster.blurb import Blurb
        >>> article = Blurb().getBlurb('da_text') # Answer random text of design article
        >>> from pagebot.elements.web.simplesite import Banner
        >>> from pagebot.elements import newTextBox
        >>> from pagebot.document import Document
        >>> siteName = 'TestDoc'
        >>> sitePath = '_export/' + siteName
        >>> doc = Document(name=siteName, w=300, h=400, padding=(30, 40, 50, 60), viewId='Mamp')
        >>> view = doc.view
        >>> #view.verbose = True
        >>> #view.doExport = False # View flag to avoid exporting to files.
        >>> page = doc[1]
        >>> banner = Banner(parent=page, cssId='Banner', fill=0.8,  margin=10, padding=10, font='Verdana')
        >>> e = newTextBox(article, parent=banner, cssClass='bannerContent', textFill=(1, 0, 1))
        >>> page.elements[0].cssId
        'Banner'
        >>> doc.export() # Export as website and open it as running in Mamp
        >>> #Try to open in a browser, assuming that there is a running local Mamp server.
        >>> result = os.system('open %s' % (view.LOCAL_HOST_URL % (doc.name, page.url)))
        """
        doInit = True

        doc = self.doc 

        rootPath = getMampPath() # Get the root path in this context where Mamp stores files.
        siteName = (doc.name or doc.title or 'UntitledSite').replace(' ','_') # Make safe site name

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

        # Copy resources to output
        for resourcePath in self.resourcePaths:
            dstPath = path
            if os.path.isdir(resourcePath):
                dstPath += resourcePath.split('/')[-1] + '/'
            if self.verbose:
                print('[MampView.build] Copy %s --> %s' % (resourcePath, dstPath))
            # TODO: Fails in Travis.
            shutil.copytree(resourcePath, dstPath)

        b = self.b # Get builder from self.doc.context of this view.
        
        if self.cssCode:
            # Add info CSS as a start.
            b.addCss(self.cssCode)

        for pn, pages in doc.pages.items():
            for page in pages:
                b.resetHtml()
                # Building for HTML, try the hook. Otherwise call by main page.build.
                hook = 'build_' + b.PB_ID # E.g. page.build_html()
                getattr(page, hook)(self, ORIGIN) # Typically calling page.build_html

                fileName = (page.fileName or page.title or page.name).replace(' ','_')
                if not fileName.lower().endswith('.html'):
                    fileName += '.html'
                if self.doExport: # View flag to avoid writing, in case of testing.
                    if not os.path.exists(path):
                        os.makedirs(path)
                    b.writeHtml(path + fileName)
        
        # Write all collected CSS into one file at destination
        if b.hasCss():
            if not os.path.exists(path):
                os.makedirs(path)
            b.writeCss(path + self.cssPath)

    def getUrl(self, name):
        u"""Answer the local URL for Mamp Pro to find the copied website."""
        return self.LOCAL_HOST_URL % (name, self.DEFAULT_HTML_FILE)


if __name__ == "__main__":
    import sys
    import doctest
    sys.exit(doctest.testmod()[0])
