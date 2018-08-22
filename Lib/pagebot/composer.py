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
#     composer.py
#
from pagebot.typesetter import Typesetter
from pagebot.elements import CodeBlock

class Composer(object):
    u"""A Composer takes a artDirection and tries to make pagination from given context,
    a “nice” layout (on existing or new document pages), by taking the elements from 
    the galley pasteboard and finding the best place in pages, e.g. in page-flows that 
    are copied from their templates.
    If necessary elements can be split, new elements can be made on the page and element can be
    reshaped byt width and height, if that results in better placements.

    >>> from pagebot.constants import A4
    >>> from pagebot.toolbox.units import em, pt
    >>> from pagebot.toolbox.color import color, blackColor
    >>> from pagebot.document import Document
    >>> h1Style = dict(font='Verdana', fontSize=pt(24), textFill=color(1, 0, 0))
    >>> h2Style = dict(font='Georgia', fontSize=pt(18), textFill=color(1, 0, 0.5))
    >>> pStyle = dict(font='Verdana', fontSize=pt(10), leading=em(1.4), textFill=blackColor)
    >>> styles = dict(h1=h1Style, h2=h2Style, p=pStyle)
    >>> doc = Document(size=A4, styles=styles)
    >>> c = Composer(doc)
    >>> md = '''## Subtitle at start\\n~~~\\npage = page.next\\n~~~\\n# Title\\n##Subtitle\\nPlain text'''
    >>> c.typeset(markDown=md)
    >>> len(c.galleys)
    1
    >>> len(c.galleys[0])
    3
    >>> doc.export('_export/ComposerTest.pdf')

    """
    def __init__(self, doc):
        self.doc = doc
        self.galleys = [] # List of galleys, e.g. each galley is content of an article.

    def typeset(self, path=None, markDown=None, styles=None):
        if styles is None:
            styles = self.doc.styles
        t = Typesetter(self.doc.context, styles=styles)
        if markDown is not None:
            path = t.markDown2FileName('/tmp/PageBot.Untitled.md', markDown)
        if path is not None:
            t.typesetFile(path)
        if t.galley: # Any input got in galley.
            self.galleys.append(t.galley)

    def compose(self, artDirection):
        u"""Compose the galley element, based on the instruction of the ArtDirection instance
        that will run the rules what content to put where.
        """
        globals = dict(composer=self, doc=self.doc, page=doc[1], style=doc.styles)        
        for galley in self.galleys:
            for e in galley.elements:
                if isinstance(e, CodeBlock):
                    e.run(globals)
                else:
            print ('---', galley)

    def XXXcompose(self, galley, page, flowId=None):
        u"""Compose the galley element, starting with the flowId text box on page.
        The composer negotiates between what the galley needs a sequential space
        for its elements, and what the page has to offer.
        If flowId is omitted, then let the page find the entry point for the first flow."""
        if flowId is None:
            flows = page.getFlows()
            assert flows # There must be at least one, otherwise error in template.
            flowId, _ = sorted(flows.keys()) # Arbitrary which one, if there are multiple entries.
        tb = page.getElementByName(flowId) # Find the seed flow box on the page, as derived from template.
        assert tb is not None # Make sure, otherwise there is a template error.
        fs = None
        # Keeping overflow of text boxes here while iterating.
        for element in galley.elements:
            if not element.isText: # This is a non-text element. Try to find placement.
                self.tryPlacement(page, tb, element)
                continue
            if fs is None:
                fs = element.fs
            else:
                fs += element.fs
            # As long as where is text, try to fit into the boxes on the page.
            # Otherwise go to the next page, following the flow, creating new pages if necessary.
            for n in range(1000): # Safety here, "while fs:" seems to be a dangerous method.
                if fs is None:
                    break
                overflow = tb.appendString(fs)
                if fs == overflow:
                    print(u'NOT ABLE TO PLACE %s' % overflow)
                    break
                fs = overflow
                if fs: # Can be None or empty
                    # Overflow in this text box, find new from (page, tbFlow)
                    page, tb = page.getNextFlowBox(tb, self.makeNewPage)
                    if tb is None: # In case here is overflow, but no next box defined in the flow.
                        print('Overflow in text, but no next flow column defined. %s' % flowId)
                        break
                else:
                    break

    def tryPlacement(self, page, tb, element):
        u"""Try to place the element on page, in relation to the current filling of tb.
        Try to pass on the template-element w/h by doing a proportional resize of the component."""
        container = page.findPlacementFor(element)
        if container is not None:
            # Replace the component on the page. Don't add to the container, because
            # that will damage the element that come from the template.
            page.replaceElement(container, element)
        else:
            print('Could not find placement for element %s.' % element)
        #else:
        #    print('TRY TO PLACE', element, element.getSize(), 'on page', page.pageNumber)


if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
