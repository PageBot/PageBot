#!/usr/bin/env python3
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
#     DrawVariableFontSkiaPointJump.py
#
#     Note: the type of animation used in this example is self-contained:
#     all code for for FontIcon class and KeyFrame class is here.
#     In the future these classes will be part of the main PageBot library,
#     which may make them incompatible with this particular example.
#
from math import radians
from pagebot import getContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance
#from pagebot.fonttoolbox.variablefontbuilder import drawGlyphPath
from pagebot.constants import CENTER
from pagebot.toolbox.color import blackColor
from pagebot.toolbox.units import em, upt

context = getContext()
W = H = 500
FRAMES = 120
f = findFont('Skia')
wghtMin, wghtDef, wghtMax = f.axes['wght']
wdthMin, wdthDef, wdthMax = f.axes['wdth']

print('wght', wghtMin, wghtDef, wghtMax)
print('wdth', wdthMin, wdthDef, wdthMax)


NORMAL = getVarFontInstance(f, dict(wght=wghtDef, wdth=wdthDef), styleName='Normal', normalize=True)
LIGHT = getVarFontInstance(f, dict(wght=wghtMin, wdth=wdthDef), styleName='Light', normalize=True)
BOLD = getVarFontInstance(f, dict(wght=wghtMax, wdth=wdthDef), styleName='Bold', normalize=True)
COND = getVarFontInstance(f, dict(wght=wghtDef, wdth=wdthMin), styleName='Cond', normalize=True)
WIDE = getVarFontInstance(f, dict(wght=wghtDef, wdth=wdthMax), styleName='Wide', normalize=True)


class FontIcon:
    W = 30
    H = 40
    L = 2
    E = 8
    LABEL_RTRACKING = em(0.02)
    LABEL_RLEADING = em(1.1)

    def __init__(self, f, name=None, label=None, title=None, eId=None, c='F', s=1, line=None,
            labelSize=10, labelFont=None, titleFont=None, x=0, y=0, show=True):
        self.f = f # Font instance
        self.labelFont = labelFont or f
        self.labelSize = labelSize
        self.titleFont = titleFont, labelFont or f
        self.title = title
        self.name = name # Name below the icon
        self.label = label # Optiona second label line
        self.c = c # Character(s) in the icon.
        self.scale = s
        self.line = line or self.L
        self.x = x
        self.y = y
        self.show = show
        self.eId = eId

    def _get_w(self):
        return self.W*self.scale
    w = property(_get_w)

    def _get_ih(self):
        """Answer scaled height of the plain icon without name label."""
        return self.H*self.scale
    ih = property(_get_ih)

    def _get_h(self):
        h = self.ih
        if self.name:
            h += self.E*self.scale*1.4 # Extra vertical space to show the name.
        if self.label:
            h += self.E*self.scale*1.4 # Extra vertical space to show the name.
        if self.title:
            h += self.E*self.scale*1.4 # Extra vertical space to show the name.
        return h
    h = property(_get_h)

    def draw(self, orgX, orgY, drawLabel=True):
        if not self.show:
            return
        w = self.w # Width of the icon
        h = self.ih # Height of the icon
        e = self.E*self.scale # Ear size
        l = self.L*self.scale # Line
        x = self.x + orgX
        y = self.y + orgY

        context.newPath()
        context.moveTo((0, 0))
        context.lineTo((0, h))
        context.lineTo((w-e, h))
        context.lineTo((w, h-e))
        context.lineTo((w, 0))
        context.lineTo((0, 0))
        context.closePath()
        context.moveTo((w-e, h))
        context.lineTo((w-e, h-e))
        context.lineTo((w, h-e))

        context.save()
        context.fill(1)
        context.stroke(0, self.line)
        context.translate(x, y)
        context.drawPath()
        bs = context.newString(self.c,
                               style=dict(font=self.f.path,
                                          textFill=blackColor,
                                          fontSize=h*2/3))
        tw, th = bs.size
        context.text(bs, (w/2-tw/2, h/2-th/3.2))

        if drawLabel:
            if self.title:
                bs = context.newString(self.title,
                                       style=dict(font=self.labelFont.path,
                     textFill=blackColor,
                                                  tracking=self.LABEL_RTRACKING,
                                                  fontSize=self.labelSize))
                tw, th = bs.size
                context.text(bs, (w/2-tw/2, self.ih+th/2))

            y -= upt(self.LABEL_RLEADING, base=self.labelSize)
            if self.name:
                bs = context.newString(self.name,
                                       style=dict(font=self.labelFont.path,
                                      textFill=blackColor,
                                      tracking=self.LABEL_RTRACKING,
                                      fontSize=self.labelSize))
                tw, th = bs.size
                context.text(bs, (w/2-tw/2, y))
                y -= upt(self.LABEL_RLEADING, base=self.labelSize)
            if self.label:
                bs = context.newString(self.label,
                                       style=dict(font=self.labelFont.path,
                                      textFill=blackColor,
                                      tracking=self.LABEL_RTRACKING,
                                      fontSize=self.labelSize))
                tw, th = bs.size
                context.text(bs, (w/2-tw/2, y))
        restore()

class KeyFrame:
    def __init__(self, objects, positions, steps=None, drawBackground=None):
        self.objects = objects
        self.positions = positions
        self.steps = steps or 1
        if drawBackground is not None:
            self.drawBacktround = drawBackground

    def drawBackground(self):
        fill(1)
        rect(0, 0, W, H)

    def draw(self):
        for n in range(self.steps):
            context.newPage(W, H)
            self.drawBackground()
            for o in self.objects:
                offsetX = 0
                offsetY = 0
                if o.eId in self.positions: # Changed target, then calculate new offset
                    tx, ty = self.positions[o.eId]
                    offsetX = (tx-o.x)*1.0*n/self.steps
                    offsetY = (ty-o.y)*1.0*n/self.steps
                o.draw(offsetX, offsetY)
        # Set the new target positions
        for o in self.objects:
            if o.eId in self.positions:
                tx, ty = self.positions[o.eId]
                o.x = tx
                o.y = ty
S = 1
labelSize = 12
C = 'Q'
print(f.axes)
skiaIcon = FontIcon(NORMAL, 'Skia', eId='Regular', c=C, s=S, labelSize=labelSize, labelFont=f, label='(1,1)')
lightIcon = FontIcon(LIGHT, 'Light', eId='Regular', c=C, s=S, labelSize=labelSize, labelFont=f, label='(0.5,1)')
boldIcon = FontIcon(BOLD, 'Bold', eId='Regular', c=C, s=S, labelSize=labelSize, labelFont=f, label='(3.2,1)')
condIcon = FontIcon(COND, 'Cond', eId='Regular', c=C, s=S, labelSize=labelSize, labelFont=f, label='(1,0.6)')
wideIcon = FontIcon(WIDE, 'Wide', eId='Regular', c=C, s=S, labelSize=labelSize, labelFont=f, label='(1,1.3)')

icons = [skiaIcon, lightIcon, boldIcon, condIcon, wideIcon]

def drawBackground(keyFrame=None, frame=None):
    d = 70
    fill(1)
    rect(0, 0, W, H)
    fill(0.9)
    rect(d, d, W-2*d, H-2*d)

def drawAnimation():
    for angle in range(0, 360, int(360/FRAMES)):
        newPage(W, H)
        drawBackground()
        x, y = 100, 360
        dSquare = 80

        radX = -sin(radians(-angle))
        radY = cos(radians(-angle))
        locRadX = -sin(radians(-angle+45))
        locRadY = cos(radians(-angle+45))

        # Reset scale drawing of all icons.
        for icon in icons:
            icon.scale = S
        # Grid
        fill(None)
        stroke(0.6)
        rect(x-dSquare+skiaIcon.w/2, y-dSquare+skiaIcon.w/2, dSquare, dSquare)
        rect(x+skiaIcon.w/2, y-dSquare+skiaIcon.w/2, dSquare, dSquare)
        rect(x-dSquare+skiaIcon.w/2, y+skiaIcon.w/2, dSquare, dSquare)
        rect(x+skiaIcon.w/2, y+skiaIcon.w/2, dSquare, dSquare)

        # Draw icons
        skiaIcon.draw(x, y)
        lightIcon.draw(x-dSquare, y)
        boldIcon.draw(x+dSquare, y)
        condIcon.draw(x, y-dSquare)
        wideIcon.draw(x, y+dSquare)

        fill(1, 0, 0, 0.5)
        stroke(None)
        markerSize = 8
        oval(x+skiaIcon.w/2+dSquare*locRadX*0.9-markerSize/2, y+skiaIcon.w/2+dSquare*locRadY*0.9-markerSize/2, markerSize, markerSize)

        px, py = 280, 220
        d = 250
        sy = 0.5
        fill(None)
        stroke(0.6)
        strokeWidth(1.5)
        # Draw Q-map
        xl, yl = px-d, py*sy
        xt, yt = px, (py+d)*sy
        xr, yr = px+d, py*sy
        xb, yb = px, (py-d)*sy
        line((xl, yl), (xt, yt))
        line((xt, yt), (xr, yr))
        line((xr, yr), (xb, yb))
        line((xb, yb), (xl, yl))
        line(((xl+xt)/2, (yl+yt)/2), ((xr+xb)/2, (yr+yb)/2))
        line(((xl+xb)/2, (yl+yb)/2), ((xr+xt)/2, (yr+yt)/2))

        bs = context.newString('Weight %0.1f' % wghtMin,
                               style=dict(font=f.path,
                                          textFill=blackColor,
                                          tracking=em(0.02),
                                          fontSize=12))
        tw, th = bs.size
        context.text(bs, ((xl+xt)/2-tw-20, (yl+yt)/2))

        bs = context.newString('Width %0.1f' % wdthMin,
                               style=dict(font=f.path,
                                          textFill=blackColor,
                                          tracking=em(0.02),
                                          fontSize=12))
        tw, th = bs.size
        context.text(bs, ((xl+xb)/2-tw-20, (yl+yb)/2))

        bs = context.newString('Width %0.1f' % wdthMax,
                               style=dict(font=f.path,
                                          textFill=blackColor,
                                          tracking=em(0.02),
                                          fontSize=12))
        context.text(bs, ((xr+xt)/2+20, (yr+yt)/2))

        bs = context.newString('Weight %0.1f' % wghtMax,
                               style=dict(font=f.path,
                                          textFill=blackColor,
                                          tracking=em(0.02),
                                          fontSize=12))
        context.text(bs, ((xb+xr)/2+20, (yb+yr)/2))

        dd = d*0.6
        stroke(0.7)
        markerSize = 16
        oval(px-(px-xl)*0.6, (py-(py-yb)*0.6-markerSize/2)*sy, (xr-xl)*0.6, (yt-yb)*0.6)

        lx, ly = px + radX*dd, sy*(py + radY*dd)

        context.fill((1, 0, 0))
        context.stroke(None)
        context.oval(lx-markerSize/2, ly-markerSize/2*sy, markerSize, markerSize*sy)

        context.stroke((1, 0, 0))
        context.fill(None)
        context.line((lx, ly), (lx, ly+20))

        for icon in icons:
            icon.scale = 0.6
        skiaIcon.draw(px-skiaIcon.w/2, py*sy, drawLabel=False)
        lightIcon.draw((xl+xt)/2-lightIcon.w/2, (yl+yt)/2, drawLabel=False)
        boldIcon.draw((xr+xb)/2-boldIcon.w/2, (yr+yb)/2, drawLabel=False)
        condIcon.draw((xl+xb)/2-condIcon.w/2, (yl+yb)/2, drawLabel=False)
        wideIcon.draw((xt+xr)/2-wideIcon.w/2, (yt+yr)/2, drawLabel=False)

        if locRadX < 0:
            wdthLoc = wdthDef + (wdthDef-wdthMin)*locRadX
        else:
            wdthLoc = wdthDef + (wdthMax-wdthDef)*locRadX
        if locRadY < 0:
            wghtLoc = wghtDef + (wghtDef-wghtMin)*locRadY
        else:
            wghtLoc = wghtDef + (wghtMax-wghtDef)*locRadY

        #wdthLoc = 1#wghtDef#locRadX
        #wghtLoc = locRadY

        bs = context.newString(('angle %0.2f rx %0.2f'
                                ' ry %0.2f wdth %0.2f'
                                ' wght %0.2f') % (angle, locRadX, locRadY,
                                                  wdthLoc, wghtLoc),
                               style=dict(font=f.path,
                                          textFill=blackColor,
                                          tracking=em(0.02),
                                          fontSize=12))
        context.text(bs, (200, 480))

        location = dict(wght=wghtLoc, wdth=wdthLoc)
        locFont = getVarFontInstance(f, location, styleName='Location', normalize=True)
        #print(locFont.info.location)
        #print(getVarLocation(f, location, normalize=False))
        """
        stroke(None)
        fill(0)
        drawGlyphPath(locFont, 'Q', lx-tw/2+20, ly+20, s=0.05, fillColor=0)
        """
        bs = context.newString('Q',
                               style=dict(font=locFont.path,
                                          textFill=blackColor,
                                          tracking=em(0.02),
                                          fontSize=80))
        tw, th = bs.size
        context.text(bs, (lx-tw/2, ly+20))

        bs = context.newString('#PageBot',
                               style=dict(font=f.path,
                                          textFill=0.5,
                                          tracking=em(0.02),
                                          fontSize=10))
        tw, th = bs.size
        context.text(bs, (W-tw-10, 10))

    saveImage('_export/SkiaPointJump.gif')

drawAnimation()


