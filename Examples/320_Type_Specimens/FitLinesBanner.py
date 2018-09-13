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
from pagebot.fonttoolbox.objects.font import findFont, Font
from pagebot.elements import *
from pagebot.elements.variablefonts.animationframe import AnimationFrame
from pagebot.document import Document
from pagebot.constants import Letter, RIGHT
from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.toolbox.units import em
from pagebot.toolbox.color import blackColor, whiteColor

class AnimatedBannerFrame(AnimationFrame):

     def drawAnimatedFrame(self, view, origin):
            """Draw the content of the element, responding to size, styles, font and content.
            Create 2 columns for the self.fontSizes ranges that show the text with and without [opsz]
            if the axis exists.

            """
            ox, oy, _ = origin
            c = self.context
            # Now make fitting text instance 
            bs = c.fitString(self.sampleText, style=self.style, w=self.w, h=self.h)
            tx, ty, _, _ = bs.bounds()
            c.text(bs, (ox-tx, oy-ty))
     
c = DrawBotContext()
W, H = 2040, 1020 # Type Network banners
M = 30
# Claire: for now, add your Fit-Variable_1.ttf to your /Library/Fonts and it can be found.
font = findFont('Fit-Variable_1')
# Fit axes to select from: here we are showing the optical size.
# Define tag list for axes to be part of the animation as sequence
sequenceAxes = ['wdth']
sequenceLength = 3 # Seconds per sequence
sequences = 2 # Amount of sequences in choreography
duration = sequenceLength * sequences # Total duration of the animation in seconds
framesPerSecond = 15 # 2 for testing
frameCnt = duration * framesPerSecond # Total number of frames
axisFrames = sequenceLength * framesPerSecond # Number of frames per axis sequence.

# Create a new doc, with the right amount of frames/pages.
doc = Document(w=W, h=H, originTop=False, frameDuration=1.0/framesPerSecond, 
    autoPages=frameCnt, context=c)
# Sample text to show in the animation
sample1 = 'Fitting' 
sample2 = 'in with'
sample3 = 'Fit'

frameIndex = 1 # Same as page index in the document
for sequenceIndex in range(sequences):
    
    for axisFrameIndex in range(axisFrames):
        page = doc[frameIndex] # Get the current frame-page
        newRect(x=0, y=0, w=page.w, h=page.h, fill=blackColor, parent=page)
        
        page.padding = M
        
        phicos = cos(radians(axisFrameIndex/axisFrames * 360))*0.5+0.5
        # Overall style for the frame
        pw = page.pw # Usable page/frame area, without paddind
        ph = page.ph
        if sequenceIndex == 0:
            x1 = 0
            y1 = ph/3 + M + ph/3*phicos
            ww1 = pw
            hh1 = ph - y1
            x2 = 0
            y2 = 0
            ww2 = pw*3/4
            hh2 = ph - hh1 - M
            x3 = ww2 + M
            y3 = 0
            ww3 = pw - x3
            hh3 = hh2
        elif sequenceIndex == 1:
            x1 = 0
            y1 = ph/3 + M + ph/3*phicos
            ww1 = pw/3 + ph*2/3*phicos
            hh1 = ph - y1
            x2 = 0
            y2 = 0
            hh2 = ph - hh1 - M
            if ww1 < pw*2/3:
                ww2 = ww1
                x3 = ww2 + M
                y3 = 0
                ww3 = pw - x3
                hh3 = ph
            else:            
                ww2 = pw/2 + pw/4*phicos
                x3 = ww2 + M
                y3 = 0
                ww3 = pw - x3
                hh3 = hh2
            
        style = dict(leading=em(1.4), font=font, xTextAlign=RIGHT, textFill=whiteColor, 
            fill=blackColor, roundVariableFitLocation=False)

        AnimatedBannerFrame(sample1, font, frameCnt, frameIndex, parent=page, style=style, 
            x=x1+M, y=y1+M, w=ww1, h=hh1, context=c)
        AnimatedBannerFrame(sample2, font, frameCnt, frameIndex, parent=page, style=style, 
            x=x2+M, y=y2+M, w=ww2, h=hh2, context=c)
        AnimatedBannerFrame(sample3, font, frameCnt, frameIndex, parent=page, style=style, 
            x=x3+M, y=y3+M, w=ww3, h=hh3, context=c)
        frameIndex += 1 # Prepare for the next frame

doc.solve()
doc.export('_export/%s_%s%s%s.gif' % (font.info.familyName, sample1, sample2, sample3))
