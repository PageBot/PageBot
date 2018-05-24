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

    DEFAULT_HTML_FILE = 'index.html'
    DEFAULT_CSS_PATH = 'css/'
    DEFAULT_CSS_FILE = 'style.css'


    #   B U I L D  H T M L  /  C S S

    def build(self, path=None, pageSelection=None, multiPage=True):
        """

        >>> from pagebot import getRootPath
        >>> from pagebot.contributions.filibuster.blurb import Blurb
        >>> blurb = Blurb()
        >>> from pagebot.elements.web.simplesite import Banner
        >>> from pagebot.elements import newTextBox
        >>> from pagebot.document import Document
        >>> siteName = 'TestDoc'
        >>> sitePath = '_export/' + siteName
        >>> doc = Document(name=siteName, w=300, h=400, autoPages=1, padding=(30, 40, 50, 60), viewId='Mamp')
        >>> view = doc.view
        >>> view
        <MampView:Mamp (0, 0)>
        >>> view.doExport = True # View flag to avoid exporting to files.
        >>> rp = getRootPath() + '/elements/web/simplesite/resources/'
        >>> view.info.resourcePaths = (rp+'js', rp+'images', rp+'fonts', rp+'css') # Directories to be copied to Mamp.        
        >>> view.info.webFontsUrl = None
        >>> page = doc[1]
        >>> page.name = view.DEFAULT_HTML_FILE
        >>> banner = Banner(parent=page, cssId='Banner', fill=(0, 1, 0))
        >>> e = newTextBox('Hello world', parent=banner, cssClass='bannerContent', textFill=(1, 0, 0))
        >>> page.elements[0].cssId
        'Banner'
        >>> doc.export()

        >>> #Try to open in a browser, assuming that there is a running local Mamp server.
        >>> result = os.system('open %s' % (view.LOCAL_HOST_URL % (doc.name, view.DEFAULT_HTML_FILE)))
        """
        doInit = True

        doc = self.doc 
        siteName = doc.name or 'UntitledSite'

        if path is None:
            path = getMampPath() + siteName + '/'
            if os.path.exists(path):
                if self.verbose:
                    print('[MampView.buils] Delete %s' % path)
                shutil.rmtree(path)
        else: # Make sure it is not there. Remove manually otherwise.
            assert path and not os.path.exists(path), 'Export site path "%s" exists: delete manually' % (path)
            if not path.endswith('/'):
                path += '/'
        cssPath = path + self.DEFAULT_CSS_PATH
        cssFilePath = cssPath + self.DEFAULT_CSS_FILE

        # Copy resources to output
        for resourcePath in self.resourcePaths:
            dstPath = path
            if os.path.isdir(resourcePath):
                dstPath += resourcePath.split('/')[-1] + '/'
            if self.verbose:
                print('[MampView.build] Copy %s --> %s' % (resourcePath, dstPath))
            # TODO: Fails in Travis.
            #shutil.copytree(resourcePath, dstPath)

        b = self.b # Get builder from self.doc.context of this view.
        # Add info CSS as a start.
        b.addCss(self.cssCode)

        for pn, pages in doc.pages.items():
            for page in pages:
                b.resetHtml()
                # Building for HTML, try the hook. Otherwise call by main page.build.
                hook = 'build_' + b.PB_ID # E.g. page.build_html()
                getattr(page, hook)(self, ORIGIN) # Typically calling page.build_html

                fileName = page.name
                if not fileName:
                    fileName = self.DEFAULT_HTML_FILE
                if not fileName.lower().endswith('.html'):
                    fileName += '.html'
                if self.doExport: # View flag to avoid writing, in case of testing.
                    if not os.path.exists(path):
                        os.makedirs(path)
                    b.writeHtml(path + fileName)
        
        # Write all collected CSS into one file at destination
        if self.cssCode:
            if not os.path.exists(cssPath):
                os.makedirs(cssPath)
            b.writeCss(cssFilePath)

    def getUrl(self, name):
        u"""Answer the local URL for Mamp Pro to find the copied website."""
        return self.LOCAL_HOST_URL % (name, self.DEFAULT_HTML_FILE)


if __name__ == "__main__":
    import sys
    import doctest
    sys.exit(doctest.testmod()[0])
