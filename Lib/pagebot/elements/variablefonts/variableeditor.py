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
#         variableeditor.py
#
import sys
from pagebot import getContext
context = getContext()
if 1 or not context.isDrawBot:
    print ('Example only runs on DrawBot.')
    sys.exit()

import AppKit
import CoreText
from vanilla import Window, Slider, TextEditor #, Button


def tagToInt(tag):
    assert len(tag) == 4
    i = 0
    for c in tag:
        i <<= 8
        i |= ord(c)
    return i

def intToTag(i):
    chars = []
    for shift in range(4):
        chars.append(chr((i >> (shift*8)) & 0xff))
    return "".join(reversed(chars))


def getFont(familyName, size=200, location=None):
    attributes = {CoreText.kCTFontFamilyNameAttribute: familyName}
    descriptor = CoreText.CTFontDescriptorCreateWithAttributes(attributes);
    if location:
        for tag, value in location.items():
            descriptor = CoreText.CTFontDescriptorCreateCopyWithVariable(descriptor, tagToInt(tag), value)
    return CoreText.CTFontCreateWithFontDescriptor(descriptor, size, [1, 0, 0, 1, 0, 0])

def getAxisInfo(fnt):
    rawAxisInfo = CoreText.CTFontCopyVariableAxes(fnt)
    axisInfo = []
    for rawInfo in rawAxisInfo:
        info = dict(
                tag=intToTag(rawInfo["NSCTVariableAxisIdentifier"]),
                name=rawInfo["NSCTVariableAxisName"],
                default=rawInfo["NSCTVariableAxisDefaultValue"],
                minValue=rawInfo["NSCTVariableAxisMinimumValue"],
                maxValue=rawInfo["NSCTVariableAxisMaximumValue"],
        )
        axisInfo.append(info)
    return axisInfo


class VarFontTextEditor:

    def __init__(self):
        self.fontName = "Bitcount Grid Single"
        fnt = getFont(self.fontName)
        axesInfo = getAxisInfo(fnt)

        self.w = Window((500, 400), "Test", minSize=(300, 200))
        # self.w.button = Button((10, 10, 120, 24), "Click", callback=self.myCallback)
        y = 10
        self.sliderMapping = {}
        for index, axisInfo in enumerate(axesInfo):
            slider = Slider((10, y, 130, 24),
                value=axisInfo['default'],
                minValue=axisInfo['minValue'],
                maxValue=axisInfo['maxValue'],
                callback=self.sliderChanged)
            self.sliderMapping[slider] = axisInfo['tag']
            setattr(self.w, "slider_%s" % index, slider)
            y += 34

        self.w.textEditor = TextEditor((150, 0, 0, 0))

        attrs = {AppKit.NSFontAttributeName: fnt}
        self.w.textEditor._textView.setTypingAttributes_(attrs)
        self.w.open()

    def sliderChanged(self, sender):
        tag = self.sliderMapping[sender]
        location = {}
        for slider, tag in self.sliderMapping.items():
            location[tag] = slider.get()
        attrs = {AppKit.NSFontAttributeName: getFont(self.fontName, location=location)}
        stor = self.w.textEditor._textView.textStorage()
        stor.setAttributes_range_(attrs, (0, stor.length()))



if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
