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
#     variable.py
#
Variable([
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
    # create a variable called 'useColor'
    # and the related ui is a CheckBox.
    dict(name="useColor", ui="CheckBox"),
    # create a variable called 'c'
    # and the related ui is a ColorWell.
    dict(name="c", ui="ColorWell")
    ], globals())
