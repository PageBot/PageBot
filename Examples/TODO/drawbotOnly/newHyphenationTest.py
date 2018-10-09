#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Example written by Frederik Berlaen
#
#     Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     testAddAttrivutesToFormattedStrings.py
#
import sys
from pagebot import getContext
context = getContext()
if not context.isDrawBot:
    print('Example only runs on DrawBot.')
    sys.exit()

from drawBot.context.baseContext import BaseContext
import CoreText
import AppKit

def justifyAttributedString(attr): 
    # create a justified copy of the attributed string
    attr = attr.mutableCopy()
    def changeParaAttribute(para, rng, _):
        para = para.mutableCopy()
        para.setAlignment_(AppKit.NSJustifiedTextAlignment)
        attr.addAttribute_value_range_(AppKit.NSParagraphStyleAttributeName, para, rng)
    
    attr.enumerateAttribute_inRange_options_usingBlock_(AppKit.NSParagraphStyleAttributeName, (0, len(attr)), 0, changeParaAttribute) 
    return attr

def getLines(attrString, path):  
    # get lines for an attribute string with a given path  
    setter = CoreText.CTFramesetterCreateWithAttributedString(attrString)
    frame = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)
    return CoreText.CTFrameGetLines(frame)

def hyphenateAttributedString(self, attrString, width=None, box=None):
    # add soft hyphens
    attrString = attrString.mutableCopy()
    mutString = attrString.mutableString()
    wordRange = AppKit.NSMakeRange(mutString.length(), 0)
    while wordRange.location > 2:
        wordRange = attrString.doubleClickAtIndex_(wordRange.location - 2)
        hyphenIndex = AppKit.NSMaxRange(wordRange)
        while hyphenIndex != AppKit.NSNotFound:
            hyphenIndex = attrString.lineBreakByHyphenatingBeforeIndex_withinRange_(hyphenIndex, wordRange)
            if hyphenIndex != AppKit.NSNotFound:
                mutString.insertString_atIndex_(unichr(self._softHypen), hyphenIndex)
    # get the path
    path = box._getCGPath()
    # get the lines
    lines = getLines(attrString, path)
    # get all lines justified
    justifiedLines = getLines(justifyAttributedString(attrString), path)
    # loop over all lines
    i = 0
    while i < len(lines):
        line = lines[i]        
        rng = CoreText.CTLineGetStringRange(line)
        subString = attrString.attributedSubstringFromRange_(rng)
        subStringText = subString.string()
        # check if the line ends with a softhypen
        if len(subStringText) and subStringText[-1] == unichr(self._softHypen):
            # here we go
            # get the justified line and get the max line width
            maxLineWidth, a, d, l = CoreText.CTLineGetTypographicBounds(justifiedLines[i], None, None, None)
            # get the last attributes
            hyphenAttr, _ = subString.attributesAtIndex_effectiveRange_(0, None)
            # create a hyphen string
            hyphenAttrString = AppKit.NSAttributedString.alloc().initWithString_attributes_("-", hyphenAttr)
            # get the width of the hyphen
            hyphenWidth = hyphenAttrString.size().width
            # get all line break location of that line
            lineBreakLocation = len(subString)
            possibleLineBreaks = [lineBreakLocation]
            while lineBreakLocation:
                lineBreakLocation = subString.lineBreakBeforeIndex_withinRange_(lineBreakLocation, (0, len(subString)))
                if lineBreakLocation:
                    possibleLineBreaks.append(lineBreakLocation)
            breakFound = False
            # loop over all possible line breaks
            while possibleLineBreaks:
                lineBreak = possibleLineBreaks.pop(0)
                # get a possible line
                breakString = subString.attributedSubstringFromRange_((0, lineBreak))
                # get the width
                stringWidth = breakString.size().width
                # add hyphen width if required
                if breakString.string()[-1] == unichr(self._softHypen):
                    stringWidth += hyphenWidth
                # found a break
                if stringWidth <= maxLineWidth:
                    breakFound = True                  
                    break
            
            if breakFound and len(breakString.string()) > 2 and breakString.string()[-1] == unichr(self._softHypen):
                # if the break line ends with a soft hyphen
                # add a hyphen
                attrString.replaceCharactersInRange_withString_((rng.location + lineBreak, 0), "-")                    
            # remove all soft hyphens for the range of that line
            mutString.replaceOccurrencesOfString_withString_options_range_(unichr(self._softHypen), "", AppKit.NSLiteralSearch, rng)
            # reset the lines, from the adjusted attribute string
            lines = getLines(attrString, path)
            # reset the justifed lines form the adjusted attributed string
            justifiedLines = getLines(justifyAttributedString(attrString), path)
        # next line        
        i += 1
    # remove all soft hyphen
    mutString.replaceOccurrencesOfString_withString_options_range_(unichr(self._softHypen), "", AppKit.NSLiteralSearch, (0, mutString.length()))
    # done!
    return attrString
  
    

s = " is a powerful, free application for MacOSX that invites you to write simple Python scripts to generate twodimensional graphics. The builtin graphics primitives support rectangles, ovals, (bezier) paths, polygons, text objects and transparency."

context.newPage(300, 700)
fff = "Times"
context.hyphenation(True)
t = context.newString('DrawBot')
print(type(t))
#t.font(fff, 15)
#t.align("right")
#t.indent(22)
#t.language("en")

#if True:
#    t.align("justified")
t += s

b = 10, 10, 202, 202

p = context.newPath()

p.moveTo((10, 10))
p.lineTo((212, 10))
p.lineTo((202, 212))
p.lineTo((14, 216))
p.closePath()

context.textBox(t, b)
context.fill(None)
context.stroke(0)
context.rect(*b)
context.translate(0, b[2]+30)

context.fill(None)
context.stroke((1, 0, 0))
#context.rect(*p)
context.drawPath(p)


#r = context.hyphenateAttributedString(BaseContext(), t.getNSObject(), box=p)
#g = context.FormattedString()
#g._attributedString = r
#print(context.textBox(g, p))
