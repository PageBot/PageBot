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
from pagebot.elements import newTextBox
from pagebot.elements import CodeBlock

class Composer:
    """A Composer takes a artDirection and tries to make pagination from given
    context, a “nice” layout (on existing or new document pages), by taking the
    elements from the galley pasteboard and finding the best place in pages,
    e.g. in page-flows that are copied from their templates.

    If necessary elements can be split, new elements can be made on the page
    and element can be reshaped byt width and height, if that results in better
    placements.

    >>> from pagebot import getResourcesPath
    >>> from pagebot.constants import A4
    >>> from pagebot.toolbox.units import em, pt
    >>> from pagebot.toolbox.color import color, blackColor
    >>> from pagebot.elements import TextBox
    >>> from pagebot.typesetter import Typesetter
    >>> from pagebot.document import Document
    >>> numPages = 4
    >>> path = getResourcesPath() + '/texts/TEST.md' # Get the path to the text markdown.
    >>> h1Style = dict(font='Verdana', fontSize=pt(36), textFill=color(1, 0, 0))
    >>> h2Style = dict(font='Georgia', fontSize=pt(18), textFill=color(1, 0, 0.5))
    >>> pStyle = dict(font='Verdana', fontSize=pt(10), leading=em(1.4), textFill=blackColor)
    >>> styles = dict(h1=h1Style, h2=h2Style, p=pStyle)
    >>> doc = Document(size=A4, styles=styles, autoPages=numPages, originTop=True)
    >>> t = Typesetter(doc.context, styles=styles)
    >>> # Create a "main" textbox in each page.
    >>> a = [TextBox(parent=doc[n], name='main', x=100, y=100, w=400, h=500) for n in range(1, numPages+1)]
    >>> galley = t.typesetFile(path)
    >>> c = Composer(doc)
    >>> targets = c.compose(galley)
    >>> targets['errors']
    []
    >>> page = doc[1]
    >>> box = page.select('main') # Get the box of this page.
    >>> box
    TextBox:main ([100pt, 100pt], [400pt, 500pt]) S(1157)
    >>> doc.export('_export/ComposerTest.pdf')

    """
    def __init__(self, doc):
        self.doc = doc

    def compose(self, galley=None, targets=None, page=None):
        """Compose the galley element, based on code blocks in the galley.

        TODO: add more art-direction instructions here.

        Targets contains the resources for the composition, such as the doc,
        current page, current box and other info that the MarkDown assumes to
        be available. If targets is omitted, then a default target dictionary 
        is created by the Composer and answered at the end.
        """
        if targets is None:
            if page is None:
                page = self.doc[1]
            
            targets = dict(composer=self, doc=self.doc, page=page, style=self.doc.styles,
                newTextBox=newTextBox)

            if page is not None:
                target['image'] = page.select('image')
                target['box'] = page.select('main'), 

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
            if isinstance(e, CodeBlock): # Code can select a new page/box and execute other Python statements.
                e.run(targets)
                verbose.append('%s.compose: Run codeblock "%s"' % (composerName, e.code[:100]))

            elif e.isTextBox:
                # In case e is a textBox, and the target box is defined, then append the content to the target.
                if targets.get('box') is None: # In case no box was selected, mark as error and move on to next element.
                    errors.append('%s.compose: No box selected. Cannot place element or copy content of %s' % (composerName, e))
                else: # TODO: Ignore empty string here? str(e.bs).strip():
                    e.parent = targets['box']
                    verbose.append('%s.compose: Add text element "%s" to text box "%s"' % (composerName, e.bs[:50], targets['box']))
              
            elif e.isLine:
                # In case e is a ruler or line, and the target box is defined, then append the content to the target.
                if targets.get('box') is None: # In case no box was selected, mark as error and move on to next element.
                    errors.append('%s.compose: No box selected. Cannot place ruler or line %s' % (composerName, e))
                else:
                    e.parent = targets['box']
                    verbose.append('%s.compose: Add ruler or line element to text box "%s"' % (composerName, targets['box']))

            elif e.isImage:
                # In case e is an image, and the target image is defined, then set the target image path.
                if targets['image'] is None: # In case no image was selected, mark as error and move on to next element
                    errors.append('%s.compose: No image selected. Cannot place element or set image path of %s' % (composerName, e))
                    e.parent = targets['image']
                    verbose.append('%s.compose: Set image element "%s" to image box' % (composerName, e.path.split('/')[-1], targets['image']))
            
            else:
                errors.append('%s.compose: No valid box or image selected "%s - %s"' % (composerName, page, e))

        return targets

    def debug(self, s):
        print('%s' % s)

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
