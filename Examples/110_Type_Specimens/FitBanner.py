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
sequences = 4 # Amount of sequences in choreography
duration = sequenceLength * sequences # Total duration of the animation in seconds
framesPerSecond = 10 # 2 for testing
frameCnt = duration * framesPerSecond # Total number of frames
axisFrames = sequenceLength * framesPerSecond # Number of frames per axis sequence.

# Create a new doc, with the right amount of frames/pages.
doc = Document(w=W, h=H, originTop=False, frameDuration=1.0/framesPerSecond, 
    autoPages=frameCnt, context=c)
# Sample text to show in the animation
sample = 'Fitting' 

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
            x = y = 0
            ww = pw/4 + pw*3/4*phicos
            hh = ph
        elif sequenceIndex == 1:
            x = y = 0
            ww = pw
            hh = ph/4 + ph*3/4*phicos
        elif sequenceIndex == 2:
            x = 0
            y = ph/2 - ph/2*phicos
            ww = pw
            hh = ph - y
        else:
            x = pw/2 - pw/2*phicos
            y = 0
            ww = pw - x
            hh = ph
            
        style = dict(leading=em(1.4), font=font, xTextAlign=RIGHT, textFill=whiteColor, 
            fill=blackColor, roundVariableFitLocation=False)

        af = AnimatedBannerFrame(sample, font, frameCnt, frameIndex, parent=page, style=style, 
            x=x+M, y=y+M, w=ww, h=hh, context=c)
        frameIndex += 1 # Prepare for the next frame

doc.solve()
doc.export('_export/%s_%s.gif' % (font.info.familyName, sample))
