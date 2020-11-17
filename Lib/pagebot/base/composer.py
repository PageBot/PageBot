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
#     composer.py
#
from pagebot.elements import newText
from pagebot.elements import CodeBlock

class Composer:
    """A Composer takes an artDirection and tries to make pagination from a
    given context, a “nice” layout (on existing or new document pages), by
    taking the elements from the galley pasteboard and finding the best place
    in pages, e.g. in page-flows that are copied from their templates.

    If necessary elements can be split, new elements can be made on the page
    and element can be reshaped byt width and height, if that results in better
    placements."""

    def __init__(self, doc):
        """
        TODO: test all target types.

        >>> from pagebot import getContext
        >>> context = getContext()
        >>> from pagebot.document import Document
        >>> doc = Document(context=context)
        >>> composer = Composer(doc)
        >>> d = composer.compose()
        """
        self.doc = doc


    def compose(self, galley=None, targets=None, page=None):
        """Compose the galley element, based on code blocks in the galley.

        TODO: add more art-direction instructions here.

        Targets contains the resources for the composition, such as the doc,
        current page, current box and other info that the MarkDown assumes to
        be available. If targets is omitted, then a default target dictionary
        is created by the Composer and answered at the end."""
        if targets is None:
            if page is None:
                page = self.doc[1]

            targets = dict(composer=self, doc=self.doc, page=page, style=self.doc.styles,
                newText=newText)

            if page is not None:
                targets['box'] = page.select('main')

        elif page is not None:
            targets['page'] = page

        if 'errors' not in targets:
            targets['errors'] = []
        errors = targets['errors']

        if 'verbose' not in targets:
            targets['verbose'] = []
        verbose = targets['verbose']

        if galley is None:
            galley = page.galley

        composerName = self.__class__.__name__

        for e in galley.elements:
            # Code can select a new page/box and execute other Python
            # statements.
            if isinstance(e, CodeBlock):
                # Keep same targets, so code blocks share sequence of altered
                # globals.
                e.run(targets)
                verbose.append('%s.compose: Run codeblock "%s"' % (composerName, e.code[:100]))

            elif targets.get('box') is not None and targets.get('box').isText and targets.get('box').bs is not None and e.isText:
                # If new content and last content are both text boxes, then
                # merge the string.
                targets.get('box').bs += e.bs

            elif targets.get('box') is not None:
                # Otherwise just paste the galley-element onto the target box.
                e.parent = targets.get('box')
            else:
                errors.append('%s.compose: No valid box or image selected "%s - %s"' % (composerName, page, e))

        return targets

    def debug(self, s):
        print('%s' % s)

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
