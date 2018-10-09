#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     testDrawVariables.py
#
import sys
from pagebot import getContext
context = getContext()
if not context.isDrawBot:
    print('Example only runs on DrawBot.')
    sys.exit()

# create small ui element for variables in the script

if __name__ == '__main__':

    w = 100
    h = 100
    x = 0
    y = 0
    useColor = True
    c = [1, 0, 0]

    context.Variable([
        # create a variable called 'w'
        # and the related ui is a Slider.
        dict(name="w", ui="Slider"),
        # create a variable called 'h'
        # and the related ui is a Slider.
        dict(name="h", ui="Slider",
                args=dict(
                    # some vanilla specific
                    # setting for a slider
                    value=100,
                    minValue=50,
                    maxValue=300)),
        # position of the rectangle
        dict(name="x", ui="Slider",
            args=dict(value=0, minValue=0, maxValue=1000)),
        dict(name="y", ui="Slider",
            args=dict(value=0, minValue=0, maxValue=1000)),
        # create a variable called 'useColor'
        # and the related ui is a CheckBox.
        # TODO Fix color checkbox and well
        #dict(name="useColor", ui="CheckBox"),
        
        # create a variable called 'c'
        # and the related ui is a ColorWell.
        #dict(name="c", ui="ColorWell")
        ], globals())

    # check if the 'useColor' variable is checked
    if useColor:
        # set the fill color from the variables
        context.fill(c)
    # draw a rect
    context.rect(x, y, w, h)
    # set the font size
    context.fontSize(h)
    # draw some text
    context.text("Hello Variable", (w, h))
