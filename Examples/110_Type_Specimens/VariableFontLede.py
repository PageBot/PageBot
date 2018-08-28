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
#     Draw animation of banner, cycling through some axes and ranges.
#     Draw the origin of the design space at the back as reference.
#

from random import random
from math import sin, cos, radians
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.elements.variablefonts.animationframe import AnimationFrame
from pagebot.document import Document
from pagebot.constants import Letter, RIGHT
from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.conditions import *
from pagebot.elements import *
from pagebot.toolbox.units import em
from pagebot.toolbox.color import whiteColor, blackColor

class AnimatedBannerFrame(AnimationFrame):

     def drawAnimatedFrame(self, view, origin):
            """Draw the content of the element, responding to size, styles, font and content.
            Create 2 columns for the self.fontSizes ranges that show the text with and without [opsz]
            if the axis exists.

            TODO: Make animation work on SVG output: https://css-tricks.com/animating-svg-css/
            """
            ox, oy, _ = origin
            c = self.context
            instance = self.f.getInstance({}) # Get neutral instance
            style = self.style.copy()

            x = 30 
            y = self.h/3+20
            xHeight = instance.info.xHeight*style['fontSize']/instance.info.unitsPerEm
            capHeight = instance.info.capHeight*style['fontSize']/instance.info.unitsPerEm
            c.stroke((0.5, 0.5, 1), 3)
            c.line((x, y), (self.w-x, y))
            c.line((x, y+xHeight), (self.w-x, y+xHeight))
            c.line((x, y+capHeight), (self.w-x, y+capHeight))

            style['font'] = instance.path
            style['textFill'] = (0.5, 0.5, 0.5, 0.7) # Opaque gray as background
            bs = c.newString(self.sampleText, style=style)
            tw, th = bs.size
            c.text(bs, (self.w/2 - tw/2, self.h/3+20))
            
            # Now make instance and draw over regular and add 
            # to new copy of the style
            
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
font = findFont('RobotoDelta-VF')
print(font.axes)
# Roboto axes to select from
# wdth - overall width
# wght - overall weight
# opsz - optical size
# YOPQ
# YTRA
# YTAS - ascender
# YTDE - descender
# YTDD
# YTUC - capitals
# YTLC - xHeight
# XTRA - change width, keep stems the same
# YTAD
# XOPQ - change stems, keep counters the same
# PWGT
# PWDT
# POPS
# GRAD - grade of stems
# UDLN

# Sample text to show in the animation
sample = 'Variety'
# Define tag list for axes to be part of the animation as sequence
axisPhases = { 
    # Fraction of the length of the animation (0..1..2) where t2-t1 < 1
    (0.4, 1.4): ('YTUC',),
    (0.5, 1.25): ('YTLC',),
    (0.6, 1.6): ('YTAS', 'YTDE'),
    (0.2, 1.1): ('wght',), 
    (0.5, 1.4): ('XTRA',),
    #(0.4, 1.3): ('opsz',)
}
duration = 4 # Duration of animation
framesPerSecond = 12
frameCnt = duration * framesPerSecond # Total number of frames in the animation

# Create a new doc, with the right amount of frames/pages.
doc = Document(w=w, h=h, originTop=False, frameDuration=1.0/framesPerSecond, 
    autoPages=frameCnt, context=c)

for frameIndex in range(frameCnt):
    page = doc[frameIndex+1] # Get the current frame-page
    location = {}
    for (a1, a2), axes in axisPhases.items():
        # Calculate the frames where this axis is working 
        da1 = int(round(frameCnt * a1))
        da2 = int(round(frameCnt * a2))
        if frameIndex < da1:
            da1 -= frameCnt
            da2 -= frameCnt # Correct for overlapping phase 
        if da2 < frameIndex:
            continue
        phasedFrameIndex = frameIndex - da1
        for axisTag in axes:
            minValue, defaultValue, maxValue = font.axes[axisTag]
            # Variable Font location for this frame sample
            phicos = cos(radians(phasedFrameIndex/(da2-da1) * 360))*-0.5+0.5
            r0 = maxValue - minValue
            r1 = minValue - defaultValue
            r2 = maxValue - defaultValue
            if r1 and r2:
                if phicos < r1/r2*0.5:
                    location[axisTag] = phicos*r2+defaultValue
                else:
                    location[axisTag] = phicos*r1+defaultValue
            elif r0:
                location[axisTag] = phicos*r0+minValue
            
    # Overall style for the frame
    style = dict(leading=em(1.4), fontSize=500, xTextAlign=RIGHT, textFill=whiteColor, 
        fill=blackColor, location=location)
    
    AnimatedBannerFrame(sample, font, frameCnt, frameIndex, parent=page, style=style, 
        w=page.w, h=page.h, context=c)
    #newTextBox('%s %s %s %s' % (da1,da2,frameIndex,location), style=dict(font='Verdana', fontSize=50, textFill=whiteColor), x=10, y=10, w=page.w, parent=page)
doc.export('_export/%s_%s.gif' % (font.info.familyName, sample))
