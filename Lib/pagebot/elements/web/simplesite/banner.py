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
#     Supporting Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     banner.py
#
from __future__ import division # Make integer division result in float.

from pagebot.elements.pbgroup import Group
from pagebot.toolbox.transformer import pointOffset

class Banner(Group):
    u"""Draw rectangle, default identical to Element itself.

    """
    def build(self, view, origin, drawElements=True):
        u"""Default drawing method just drawing the frame.
        Probably will be redefined by inheriting element classes.

        >>> import os
        >>> from pagebot.document import Document
        >>> from pagebot.elements import newTextBox
        >>> doc = Document(viewId='Page')
        >>> page = doc[1]
        >>> page.title = 'Banner Test'
        >>> page.name = 'index'
        >>> banner = Banner(parent=page, cssId='ThisBannerId', w=500, h=100, fill=0.2)
        >>> tb = newTextBox('This is a banner.', parent=banner)
        >>> doc.export('_export/BannerTest.pdf')
        """
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        self.buildFrame(view, p) # Draw optional frame or borders.

        # Let the view draw frame info for debugging, in case view.showElementFrame == True
        view.drawElementFrame(self, p) 

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin) # Depends on flag 'view.showElementInfo'

    def build_html(self, view, origin=None, drawElements=True):
        u"""Build the HTML/CSS navigation, depending on the pages in the root document.

        Typical HTML export
        <div id="banner">   
            ...     
        </div>

        >>> import os
        >>> from pagebot.document import Document
        >>> from pagebot.elements import newTextBox
        >>> doc = Document(viewId='Mamp')
        >>> view = doc.view
        >>> page = doc[1]
        >>> page.title = 'Banner Test'
        >>> page.name = 'index'
        >>> banner = Banner(parent=page, cssId='ThisBannerId')
        >>> tb = newTextBox('This is a banner.', fontSize=24, parent=banner)
        >>> doc.export() # Mamp-view knows where it goes
        >>> # Try to open in browser. It works if a local server (like MAMP) runs for page.url.
        >>> result = os.system('open %s' % (view.LOCAL_HOST_URL % (doc.name, page.url)))
        """
        b = view.context.b
        self.build_css(view)
        b.div(cssClass=self.cssClass, cssId=self.cssId)
        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, origin)

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, origin)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, origin)

        b._div()

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
