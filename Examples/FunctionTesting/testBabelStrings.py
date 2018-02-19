#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     testBabelStrings.py
#
# Test BabelString both under DrawBotContext and FlatContext
from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.contexts.flatcontext import FlatContext

testContexts = (
    (DrawBotContext(), '_export/testFlatString.pdf'),
    # TODO: Get this to work with Flat
    #(FlatContext(), '_export/testDrawBotString.pdf'),
)
for context, path in testContexts:
    # Create a new BabelString with the DrawBot FormttedString inside.
    style=dict(font='Verdana', fontSize=50, textFill=(1, 0, 0))
    bs = context.newString('This is a string', style=style)
    # It prints it content.
    print bs
    # Adding or appending strings are added to the internal formatted string.
    bs += ' and more'
    print bs
    # Usage in DrawBot by addressing the embedded FS for drawing.
    context.text(bs, (100, 100))
    context.saveImage(path)