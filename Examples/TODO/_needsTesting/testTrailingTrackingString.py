# This script shows the behavior of FormattedStrings in DrawBot Context.
# Tracking is added after the glyphs, so the measured width of a tracked
# string is wider that it looks.
# To safely measure the real width of the string, the width of one "track"
# needs to be subtracted.

from pagebot import getContext
from pagebot.toolbox.units import em

context = getContext()

# Create a new page
w, h = 400, 100
context.newPage(w, h)

# Draw vertical line in the middle of the page as reference.
context.fill(None)
context.strokeWeight=0.5
context.stroke((0, 0, 0.4))
context.line((w/2, 0), (w/2, h))

TRACKING = em(0.05)
FONT_SIZE = 14
TRACKED_SPACE = FONT_SIZE * TRACKING

# New Babel string, probably DrawBot FormattedString flavor.
bs = context.newString('TRACKEDSTRING', style=dict(font='Verdana',
    fontSize=FONT_SIZE, tracking=TRACKING))
# Call DrawBot textSize to determine the size of the string
# including the tracking
tw, th = bs.size

context.text(bs, (w/2 - tw/2, 60))
context.stroke((1,0,0))
context.rect(w/2-tw/2, 60, tw, th)

print(TRACKED_SPACE)

tw -= TRACKED_SPACE

context.text(bs, (w/2 - tw/2, 20))
context.stroke((1,0,0))
context.rect(w/2-tw/2, 20, tw, th)
