# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     basehtmlcssbuilder.py
#
from pagebot.builders.basebuilder import BaseBuilder

class BaseHtmlCssBuilder(BaseBuilder):

    def build(self, e, view):
        u"""
        Builds the header of an HTML document.
        Note that the inheriting PhPBuilder uses the result of this method to generate
        the header.php file, as a separate result stream.
        """
        self.docType(self.ID)
        self.html()
        self.head()
        # Title depends on selected article. Otherwise show the path, if not available.
        path = self.getPath()
        title = component.getTitle(path=path) or path
        self.title_(title) # Search for the title in the component  tree
        self.ieExceptions()
        # self.supportMediaQueries() # Very slow, getting this from Google?
        self.setViewPort()
        self.buildFontLinks(component)
        self.buildCssLinks(component)
        self.ieExceptions()
        # Build required search engine info, if available in self.adapter
        self.buildMetaDescription(component)
        self.buildMetaKeyWords(component)

        self.link(rel="apple-touch-icon-precomposed", href="img/appletouchicon.png")
        self.buildJavascript(component)
        self.buildFavIconLinks(component)
        self._head()

        self.body()
        # Instead of calling the main self.block
        self.div(class_='page_' + component.name or component.class_ or self.C.CLASS_PAGE)
        self.comment(component.getClassName()) # Add reference  Python class name of this component


        u"""Build the tail of an HTML document.
        Note that the inheriting PhPBuilder uses the result of this method to generate
        the footer.php file, as a separate result stream."""
        # Instead of calling the main self._block
        if self.isEditor(): # In case we are live in /edit mode, make the whole page as form.
            self._editor(component)
        self._div(comment='.page_'+(component.name or component.class_ or self.C.CLASS_PAGE))
        self._body()
        self._html()

