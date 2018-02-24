# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Free to use. Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     businessCardsByDraw.py
#
from pagebot.contexts import defaultContext as context
from pagebot.contexts.platform import getRootPath
from pagebot.style import USBusinessCard, CENTER, DISPLAY_BLOCK, RIGHT, LEFT

# Standard USA Businesscard format, defined in pagebot.style
W, H = USBusinessCard
M = 4 # Padding of the page

# Get the root of the PageBot directory, to find the demo images.
ROOT_PATH = getRootPath()

def buildBusinessCard(w, h):
	
    
    for imageIndex in range(1, 5):

        context.newPage(w, h) 
        
        y = h # Start vertical position on top of the page.
    
        # Draw one of the 4 Bitcount background images, filename indexed by imageIndex
        # The TYPETR Bitcount license can be purchased at:
        # https://store.typenetwork.com/foundry/typetr/fonts/bitcount
        imagePath = ROOT_PATH + '/Examples/Portfolios/images/BitcountRender%d.png' % imageIndex
        context.image(imagePath, (0, 0), w=w) # Set to full page width at origin
    
        # Define some style. Note thate TYPETR Upgrade is the identity typeface, which may not be installed.
        # Another font is selected in case TYPETR Upgrade is not available.
        # View more here: https://upgrade.typenetwork.com
        # A license can be purchased at:
        # https://store.typenetwork.com/foundry/typetr/fonts/upgrade
        style = dict(font='Upgrade-Regular', fontSize=14, textFill=1, xTextAlign=CENTER)
        styleTitle = dict(font='Upgrade-Italic', fontSize=10, textFill=1, xTextAlign=CENTER)
        styleEmail = dict(font='Upgrade-Light', fontSize=8, textFill=1, xTextAlign=CENTER, leading=10, rTracking=0.02)
        # Create styled BabelString for the name lines
        bs = context.newString('Petr van Blokland\n', style=style)  
        bs += context.newString('Designer | Educator | Founder\n', style=styleTitle)  
        bs += context.newString('buro@petr.com | @petrvanblokland', style=styleEmail)
        # Get the size of the text block, to position it centered
        tw, th = context.textSize(bs)  
        # Draw a textbox in the contextf canvas.
        context.text(bs, (w/2-tw/2, h*0.55))

        # Create a style for the logo. The size and tracking is hardcoded to fit the business card width.
        logoStyle = dict(font='Upgrade-Black', fontSize=22, textFill=1, rTracking=1.4)
        # Create the BabelString, containing the fitting logo with tracking.
        bs = context.newString(u'.TYPETR', style=logoStyle)
        # Get the size of the text block, to position it centered
        tw, th = bs.size()
        # Draw a textbox in the contextf canvas.
        context.text(bs, (w/2-tw/2-3, 2*M)) 
 
# Draw the 4 busines cards with different backgrounds.
buildBusinessCard(W, H)

#saveImage('_export/businessCards.png', multipage=True)
saveImage('_export/businessCards.pdf', multipage=True)
