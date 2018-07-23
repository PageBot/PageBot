# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
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
from __future__ import division

from random import random
from math import sin, cos, radians
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.elements.variablefonts.animationframe import AnimationFrame
from pagebot.document import Document
from pagebot.constants import Letter, RIGHT
from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.conditions import *

class AnimatedBannerFrame(AnimationFrame):

     def drawAnimatedFrame(self, view, origin):
            """Draw the content of the element, responding to size, styles, font and content.
            Create 2 columns for the self.fontSizes ranges that show the text with and without [opsz]
            if the axis exists.

            """
            ox, oy, _ = origin
            c = self.context
            # Make the instance for the style holding the location
            style = self.style.copy()
            instance = self.f.getInstance(self.style['location'])#instance.path
            style['font'] = instance.path

            # Draw the growing text on the right in the real font size enlarged by fontSizeFactor
            bs = c.newString(self.sampleText, style=style)
            tw1, th1 = bs.textSize()
            x1, y1 = self.w*2/3, self.h/2-th1/4
            c.text(bs, (x1, y1))
                  
            # Magnifying glass 
            R = 320
            L = 40
            c.stroke((0.6, 0.8, 1, 0.9), L)
            c.fill(None)
            x = x1-R/2+R/8
            y = self.h/2-R/2
            c.oval(x, y, R, R)
            c.line((x-L/2+2, y+R/2), (x-R+2*L, y+R/2))
       
            # Large "Opt" on the left
            style['fontSize'] = self.f.axes['opsz'][2]*magnifySizeFactor
            bs = c.newString(self.sampleText[:3], style=style)
            tw2, th2 = bs.textSize()
            x2, y2 = self.w/2-tw2, self.h/2-th2/5
            c.text(bs, (x2, y2)) # Make tekst right aligned
     
c = DrawBotContext()
W, H = 2040, 1020 # Type Network banners
font = findFont('AmstelvarAlpha-VF')
# Amstelvar axes to select from: here we are showing the optical size.
# Define tag list for axes to be part of the animation as sequence
sequenceAxes = ['opsz']
sequenceLength = 3 # Seconds per sequence
sequences = len(sequenceAxes) # Amount of sequences, one per axis
duration = sequenceLength * len(sequenceAxes) # Total duration of the animation in seconds
framesPerSecond = 10
frameCnt = duration * framesPerSecond # Total number of frames
axisFrames = sequenceLength * framesPerSecond # Number of frames per axis sequence.

fontSizeFactor = 3 # Enlarge the [opsz] font size by this factor.
magnifySizeFactor = 8 # Enlarge magnified word by this factor, compared to the max value of [opsz]

# Create a new doc, with the right amount of frames/pages.
doc = Document(w=W, h=H, originTop=False, frameDuration=1.0/framesPerSecond, 
    autoPages=frameCnt, context=c)
# Sample text to show in the animation
sample = 'Optical size' #font.info.familyName #'Decovar'

frameIndex = 1 # Same as page index in the document
for axisTag in sequenceAxes:

    minValue, defaultValue, maxValue = font.axes[axisTag]
    for axisFrameIndex in range(axisFrames):
        page = doc[frameIndex] # Get the current frame-page
        page.w = W

        phisin = sin(radians(axisFrameIndex/axisFrames * 360+3/4*360))*0.5+0.5
        fontSize = phisin*(maxValue - minValue) + minValue

        # Variable Font location for this frame sample
        location = {axisTag: fontSize}
        # Overall style for the frame
        style = dict(rLeading=1.4, fontSize=fontSize*fontSizeFactor, xTextAlign=RIGHT, textFill=1, 
            testStroke=None,
            fill=0, location=location)
        
        af = AnimatedBannerFrame(sample, font, frameCnt, frameIndex, parent=page, style=style, 
            w=page.pw, h=page.ph, context=c)
        frameIndex += 1 # Prepare for the next frame

doc.solve()
doc.export('_export/%s_%s.gif' % (font.info.familyName, sample))
