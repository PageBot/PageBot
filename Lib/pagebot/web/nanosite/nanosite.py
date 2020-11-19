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
#     nanpsite.py
#
#     NanoSite is a simple basix website generator.
#
import os
import shutil
import traceback
from sys import platform

from pagebot import getContext
from pagebot.constants import *
from pagebot.base.composer import Composer
from pagebot.base.typesetter import Typesetter
from pagebot.elements import *
from pagebot.elements.views import MampView
from pagebot.elements.web.nanosite.siteelements import *
from pagebot.filepaths import getMampPath
from pagebot.web.basesite import BaseSite

class NanoSite(BaseSite):
    """NanoSite implements a bacic website generator class, that can be used to
    inherit from or as example how to make website publication classes.

    >>> import os
    >>> from pagebot.filepaths import getResourcesPath
    >>> from pagebot.themes import BackToTheCity
    >>> from css.nanostyle_css import cssPy
    >>> name = 'PageBot NanoSite'
    >>> # Pick a theme for this site.
    >>> theme = BackToTheCity()
    >>> # Get example markDown file from resources.
    >>> srcPath = getResourcesPath() + '/texts/SITE.md'
    >>> os.path.exists(srcPath)
    True
    >>> ns = NanoSite(name=name, theme=theme)
    >>> doc = ns.produce(srcPath, cssPy=cssPy, spellCheck=True, doOpen=False)
    >>> doc
    <Document "PageBot NanoSite" Pages=6 Templates=1 Views=1>
    """
    DEFAULT_VIEW_ID = MampView.viewId

    def makeNavigation(self, doc):
        """After all pages of the site are generated, we can use the compiled
        page tree from doc to let all Navigation elements build the menu for
        each page.

        """
        for pages in doc.pages.values():
            for page in pages:
                navigation = page.select('Navigation')
                if navigation is not None:
                    # Get a fresh one for each page.
                    navigation.pageTree = doc.getPageTree()

    def makeTemplate(self, doc):
        """Make a default template that is the typical base for a NanoSite.
        More details can be filled by the source markDown file."""

        default = Template('Default', context=doc.context)
        # Create main page wrapper.
        wrapper = Wrapper(parent=default)

        # Header to hold logo and navigation elements.
        header = Header(parent=wrapper)

        #logoString = doc.context.newString(SITE_NAME)
        Logo(parent=header, logo=doc.title)
        BurgerButton(parent=header)

        # Responsive conditional menus.
        Navigation(parent=header)
        MobileMenu(parent=header)

        # Just make a simple content container in this template. Rest of
        # content is created upon request in MarkDown
        Content(parent=wrapper)

        # Default Footer at bottom of every page.
        Footer(parent=wrapper)

        doc.addTemplate('default', default)
        return default

    def produce(self, srcPaths, viewId=None, cssPy=None, resourcePaths=None,
            cssUrls=None, defaultImageWidth=None, name=None, title=None,
            theme=None, verbose=False, spellCheck=False, doOpen=True, **kwargs):
        """Create a Document with the current settings of self. Then build the
        document using the defined view (detault is MampView.viewId) to make
        the Mamp site. Finally answer the created Document instance."""
        if defaultImageWidth is None:
            defaultImageWidth = MAX_IMAGE_WIDTH
        if theme is None:
            theme = self.theme
        if not isinstance(srcPaths, (list, tuple)):
            srcPaths = [srcPaths]

        context = getContext('Html')
        doc = self.newDocument(viewId=viewId or self.DEFAULT_VIEW_ID,
                autoPages=1, defaultImageWidth=defaultImageWidth, name=name or
                self.name, title=title or self.title, theme=theme, context=context, **kwargs)

        # Write the CSS, set the view css paths and translate cssPy into css
        # source file.
        view = doc.view
        view.resourcePaths = resourcePaths or ['css']
        view.cssUrls = cssUrls or ['css/normalized.css']

        if cssPy is not None:
            p = os.path.abspath(__file__)
            base = '/'.join(p.split('/')[:-1])
            # Generate css by mapping theme.mood on cssPy.
            cssPath = '%s/css/nanostyle_py.css' % base
            view.cssUrls.append(cssPath)

            try:
                doc.context.b.writeCss(cssPath, cssPy % doc.theme.mood)
            except:
                # Travis crashes on relative path.
                print(traceback.format_exc())

        # Make the all pages and elements of the site as empty containers, that
        # then can be selected and filled by the composer, using the galley
        # content. Of the MarkDown text can decide to create new elements
        # inside selected elements.
        template = self.makeTemplate(doc)

        page = doc[1]
        # Copy element tree to page.
        page.applyTemplate(template)

        # By default, the typesetter produces a single Galley with content and
        # code blocks.
        t = Typesetter(doc.context)
        for srcPath in srcPaths:
            galley = t.typesetFile(srcPath)

        # Creates a Composer for this document, then create pages and fill
        # content.
        composer = Composer(doc)

        # The composer executes the embedded Python code blocks that indicate
        # where content should go. by the HtmlContext. Feedback by the code
        # blocks is added to verbose and errors list
        targets = dict(doc=doc, page=page, template=template)
        composer.compose(galley, targets=targets)

        if verbose:
            if targets['verbose']:
                print('Verbose\n', '\n'.join(targets['verbose']))
            # In case there are any errors, show them.
            if targets['errors']:
                print('Errors\n', '\n'.join(targets['errors']))

        # Find the navigation elements and fill them, now we know all the
        # pages.
        self.makeNavigation(doc)

        if spellCheck:
            # https://www.hyphenator.net/en/word/...
            unknownWords = doc.spellCheck(LANGUAGE_EN)
            if unknownWords:
                print(unknownWords)

        view = doc.view


        mampPath = getMampPath()
        siteName =  doc.name.replace(' ', '_')
        filePath = mampPath + siteName

        if verbose:
            print('Site path: %s' % filePatah)

        if os.path.exists(filePath):
            # Comment this line, if more safety is required. In that case
            # manually delete.
            shutil.rmtree(filePath)

        doc.export(filePath)

        if doOpen:
            url = view.getUrl(siteName)
            os.system(u'/usr/bin/open "%s"' % url)

        return doc

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
