# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in Drawbot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     composer.py
#
from drawBot import FormattedString

class Composer(object):
    u"""A Composer takes a galley and tries to make a “nice” layout (on existing or new document pages),
    by taking the elements from the galley pasteboard and finding the best place in pages, e.g. in
    page-flows that are copied from their templates.
    If necessary elements can be split, new elements can be made on the page and element can be
    reshaped byt width and height, if that results in better placements.
    """
    def __init__(self, document):
        u"""Store the document that this Composer will be operating on. The document inclused
        the pages that already exist, and it defined the baseStyle for all other cascading styles."""
        self.document = document

    def compose(self, galley, page, flowId=None):
        u"""Compose the galley element, starting with the flowId text box on page.
        The composer negotiates between what the galley needs a sequential space
        for its elements, and what the page has to offer.
        If flowId is omitted, then let the page find the entry point for the first flow."""
        if flowId is None:
            flows = page.getFlows()
            assert len(flows) # There must be at least one, otherwise error in template.
            flowId, _ = sorted(flows.keys()) # Arbitrary which one, if there are multiple entries.
        tb = page.getElement(flowId) # Find the seed flow box on the page, as derived from template.
        assert tb is not None # Make sure, otherwise there is a template error.
        fs = FormattedString('')
        # Keeping overflow of text boxes here while iterating.
        for element in galley.elements:
            if not element.isText: # This is a non-text element. Try to find placement.
                self.tryPlacement(page, tb, element)
                continue
            fs += element.fs
            # As long as where is text, try to fit into the boxes on the page.
            # Otherwise go to the next page, following the flow, creating new pages if necessary.
            for n in range(10000): # Safety here, "while fs:" seems to be a dangerous method.
                overflow = tb.append(fs)
                if fs == overflow:
                    print(u'NOT ABLE TO PLACE %s' % overflow)
                    break
                fs = overflow
                if len(fs):
                    # Overflow in this text box, find new from (page, tbFlow)
                    page, tb = page.getNextFlowBox(tb)
                    assert tb is not None # If happens, its a mistake in one of the templates.
                else:
                    break

    def tryPlacement(self, page, tb, element):
        u"""Try to place the element on page, in relation to the current filling of tb."""
        container = page.findPlacementFor(element)
        if container is not None:
            page.replaceElement(container, element)
        else:
            print('Could not find placement for', element)
        #else:
        #    print 'TRY TO PLACE', element, element.getSize(), 'on page', page.pageNumber
