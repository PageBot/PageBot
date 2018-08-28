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
from pagebot.toolbox.units import em

class AnimatedBannerFrame(AnimationFrame):

     def drawAnimatedFrame(self, view, origin):
            """Draw the content of the element, responding to size, styles, font and content.
            Create 2 columns for the self.fontSizes ranges that show the text with and without [opsz]
            if the axis exists.

            """
            ox, oy, _ = origin
            c = self.context #makes copy of style
            
            style = self.style.copy()
            instance = self.f.getInstance(style['location'])
            style['font'] = instance
            bs = c.newString(self.sampleText, style=style)
            tw, th = bs.size
            c.text(bs, (self.w/2 - tw/2, self.h/2-th/8)) # /8 vert
            
            style['fontSize'] = style['location']['opsz'] * 4
            style['font'] = instance
            bs = c.newString('%s %dpt' % (self.sampleText, style['fontSize']), style=style)
            tw, th = bs.size
            c.text(bs, (self.w/2 - tw/2, self.h/4-th/8)) 
     
c = DrawBotContext()
W, H = 2040, 1020 # Type Network banners

# Claire: for now, add your Fit-Variable_1.ttf to your /Library/Fonts and it can be found.
#Gimlet_Italics-VF.ttf
#Gimlet_Romans-VF.ttf
font = findFont('AlliumMediumVARGX_hyphen')
print(font)
# Fit axes to select from: here we are showing the optical size.
# Define tag list for axes to be part of the animation as sequence
sequenceAxes = ['opsz']
sequenceLength = 3 # Seconds per sequence
sequences = len(sequenceAxes) # Amount of sequences, one per axis
duration = sequenceLength * len(sequenceAxes) # Total duration of the animation in seconds
framesPerSecond = 12
frameCnt = duration * framesPerSecond # Total number of frames
axisFrames = sequenceLength * framesPerSecond # Number of frames per axis sequence.

# Create a new doc, with the right amount of frames/pages.
doc = Document(w=W, h=H, originTop=False, frameDuration=1.0/framesPerSecond, 
    autoPages=frameCnt, context=c)
# Sample text to show in the animation
sample = 'Magnetic' 

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
        style = dict(leading=em(1.4), fontSize=300, textFill=(0, 0, 0), 
            fill=.8, location=location)
            
        print (style)
        
        af = AnimatedBannerFrame(sample, font, frameCnt, frameIndex, parent=page, style=style, 
            w=page.w, h=page.h, context=c)
        frameIndex += 1 # Prepare for the next frame
        

doc.solve()
doc.export('_export/%s_%s.gif' % (font.info.familyName, sample))
