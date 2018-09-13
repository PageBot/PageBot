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

from random import random
from math import sin, cos, radians
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.elements.variablefonts.animationframe import AnimationFrame
from pagebot.document import Document
from pagebot.constants import Letter, RIGHT
from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.conditions import *
from pagebot.toolbox.color import Color, color, blackColor
from pagebot.toolbox.units import em

class AnimatedBannerFrame(AnimationFrame):

     def drawAnimatedFrame(self, view, origin):
            """Draw the content of the element, responding to size, styles, font and content.
            Create 2 columns for the self.fontSizes ranges that show the text with and without [opsz]
            if the axis exists.

            """
            ox, oy, _ = origin
            c = self.context
            style = self.style.copy()

            instance = self.f.getInstance({}) # Get neutral instance
            style['font'] = instance.path
            style['textFill'] = Color(0.5, 0.5, 0.5, 0.7) # Opaque gray as background
            bs = c.newString(self.sampleText, style=style)
            tw, th = bs.size
            c.text(bs, (self.w/2 - tw/2, self.h/3+20))
            
            # Now make instance and draw over regular and add to new copy of the style
            style = self.style.copy()
            instance = self.f.getInstance(self.style['location'])
            style['font'] = instance.path
            #print(self.frameIndex, style['font'])
            #style['fontSize'] = self.h/3
            bs = c.newString(self.sampleText, style=style)
            tw, th = bs.size
            c.text(bs, (self.w/2 - tw/2, self.h/3+20))
       

c = DrawBotContext()
w, h = 2040, 1020 # Type Network banners
font = findFont('DecovarAlpha-VF')
# Decovar axes to select from
# 'BLDA' Inline
# 'TRMG' Serif terminals
# 'BLDB' Turning flourishes
# 'SKLA' Blocked inside
# 'SKLD' Striped stems
# 'TRMA' Rounded
# 'SKLB' Turning round flourishes
# 'TRMC' Round terminal serifs
# 'TRMB' Sharp terminal serifs
# 'TRME' Split sharp terminal serifs
# 'TRMD' Angled terminals
# 'WMX2' Contrast width black
# 'TRMF' Plus terminals
# 'TRMK' Rectangle inside terminal
# 'TRML' Diamond inside terminal
 

# Define tag list for axes to be part of the animation as sequence
sequenceAxes = ['TRMC', 'SKLD', 'TRMG', 'BLDB']
#sequenceAxes = ['SKLD', 'BLDB', 'TRMK', 'BLDA']
sequenceLength = 3 # Seconds per sequence
sequences = len(sequenceAxes) # Amount of sequences, one per axis
duration = sequenceLength * len(sequenceAxes) # Total duration of the animation in seconds
framesPerSecond = 10
frameCnt = duration * framesPerSecond # Total number of frames
axisFrames = sequenceLength * framesPerSecond # Number of frames per axis sequence.

# Create a new doc, with the right amount of frames/pages.
doc = Document(w=w, h=h, originTop=False, frameDuration=1.0/framesPerSecond, 
    autoPages=frameCnt, context=c)
# Sample text to show in the animation
sample = font.info.familyName #'Decovar'

frameIndex = 1 # Same as page index in the document
for axisTag in sequenceAxes:

    minValue, defaultValue, maxValue = font.axes[axisTag]
    for axisFrameIndex in range(axisFrames):
        page = doc[frameIndex] # Get the current frame-page
        axisRange = maxValue - minValue
        phisin = sin(radians(axisFrameIndex/axisFrames * 360+3/4*360))*0.5+0.5
        
        # Variable Font location for this frame sample
        location = {axisTag: phisin*axisRange+minValue}
        # Overall style for the frame
        style = dict(leading=em(1.4), fontSize=400, xTextAlign=RIGHT, textFill=color(1), 
            fill=blackColor, location=location)
        
        af = AnimatedBannerFrame(sample, font, frameCnt, frameIndex, parent=page, padding=20, style=style, 
            w=page.pw, h=page.ph, context=c)
        frameIndex += 1 # Prepare for the next frame


doc.export('_export/%s_%s.gif' % (font.info.familyName, sample))
