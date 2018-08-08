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
            c = self.context
            style = self.style.copy()
            phisin = sin(radians(self.frameIndex/self.frames * 360))
            phicos = cos(radians(self.frameIndex/self.frames * 360))

            for tag, (axisMin, axisDefault, axisMax) in self.f.axes.items():
                wdthRange = wdthMax - wdthMin
                wghtRange = wghtMax - wghtMin
                location = dict(wdth=phisin*wdthRange/2+wdthRange/2+wdthMin, wght=phisin*wghtRange/2+wghtRange/2+wghtMin)
                instance = self.f.getInstance(location)#instance.path
                style['font'] = instance.path
                #print(self.frameIndex, style['font'])
                #style['fontSize'] = self.h/3
                bs = c.newString(self.sampleText, style=style)
                tw, th = bs.size
                c.text(bs, (self.w/2 - tw/2, self.h/2))
                            
                wghtMin, wghtDefault, wghtMax = self.f.axes['wght']

                """
            #location = getScaledLocation(self.f, dict(wght=self.frameIndex/self.frames))
            #instance = getInstance(self.f, location)
            phisin = sin(radians(self.frameIndex/self.frames * 360))
            phicos = cos(radians(self.frameIndex/self.frames * 360))

            style['textFill'] = 1-phicos*0.3+0.5 
            # TODO: Not the right instance-weight is shown in export.
            wdthRange = wdthMax - wdthMin
            wghtRange = wghtMax - wghtMin
            location = dict(wdth=phisin*wdthRange/2+wdthRange/2+wdthMin, wght=phisin*wghtRange/2+wghtRange/2+wghtMin)
            instance = self.f.getInstance(location)#instance.path
            style['font'] = instance.path
            #print(self.frameIndex, style['font'])
            #style['fontSize'] = self.h/3
            bs = c.newString(self.sampleText, style=style)
            tw, th = bs.size
            c.text(bs, (self.w/2 - tw/2, self.h/2))



            glyph = instance['H']
            c.save()
            c.stroke(0, 0.25)
            gray = phisin*0.3+0.5 
            c.fill((gray, gray, 1-gray, 0.6))
            s = 0.45
            c.scale(s)
            c.drawPath(glyph.path, ((ox+self.pl)/s, (oy+self.ph/4)/s))
            c.restore()
            """
            
            """
            path = "/Users/petr/Desktop/TYPETR-git/TYPETR-Bitcount-Var/variable_ttf/BitcountTest_DoubleCircleSquare4-VF.ttf"
            f = Font(path)
            SHPEMin, SHPEDefault, SHPEMax = f.axes['SHPE']
            SHPERange = SHPEMax - SHPEMin
            wghtMin, wghtDefault, wghtMax = self.f.axes['wght']
            wghtRange = wghtMax - wghtMin
            location = dict(SHPE=phisin*SHPERange/2+SHPERange/2+SHPEMin, wght=phicos*wghtRange/2+wghtRange/2+wghtMin)
            instance = f.getInstance(location)#instance.path
            glyph = instance['px']
            c.save()
            c.stroke(0, 0.25)
            gray = phisin*0.3+0.5 
            c.fill((1-gray, gray, gray, 0.6))
            s = 5
            c.scale(s)
            c.drawPath(glyph.path, ((ox+self.w/2+self.pl)/s, (oy+self.ph/4)/s))
            c.restore()

            """
   
c = DrawBotContext()
w, h = 2040, 1020 # Type Network banners
font = findFont('DecovarAlpha-VF')

sequenceAxes = font.axes.keys()
sequenceLength = 3 # Seconds per sequences
sequences = len(sequenceAxes)
duration = sequenceLength * sequenceAxes # Total duration of animation
framesPerSecond = 10
frames = duration * framesPerSecond # Total number of frames
axisFrames = sequenceLength * framesPerSecond

doc = Document(w=w, h=h, originTop=False, frameDuration=1/framesPerSecond, 
    autoPages=frames, context=c)
sample = font.info.familyName #'Decovar'

pn = 1
for axisTag in font.axes.keys():
    axisFrames = 
    minValue, defaultValue, maxValue = font.axes[axisTag]
    for frameIndex in range(1, len(font.axes)):
        page = doc[pn]
        axisRange = maxValue - minValue
        phisin = sin(radians(frameIndex/self.frames * 360))
        phicos = cos(radians(self.frameIndex/self.frames * 360))
        
        location = {phisin*wdthRange/2+wdthRange/2+wdthMin, wght=phisin*wghtRange/2+wghtRange/2+wghtMin)
        style = dict(leading=em(1.4), fontSize=400, xTextAlign=RIGHT, fill=blackColor)
        af = AnimatedBannerFrame(font, frames, pn, parent=page, padding=20, style=style, 
            sampleText=sample, w=page.pw, h=page.ph, context=c)
        pn += 1


doc.export('_export/%s_%s.gif' % (font.info.familyName, sample))
