# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     family.py
#
#     Implements a family collestion of Style instances.
#
class Family(object):
    def __init__(self, name):
        self.name = name
        self.fonts = {} # Key is font name. Value is Font instances.

    def __len__(self):
        return len(self.fonts)
        
    def addFont(self, font):
        assert not font.info.styleName in self.fonts, ('Font "%s" already in family "%s"' % (font.info.styleName, self.fonts.keys()))
        self.fonts[font.info.styleName] = font
        
    def getRegularFont(self):
        # Answer the style that has width/weight closest to 500 and angle is closest to 0
        targetWeight = targetWidth = 500
        targetAngle = 0
        regularFont = None
        for font in self.fonts.values(): # Scan through all, no particular oder.
            if font is None: # Take the first to compare with.
                regularFont = font
                continue
            # Find style that has width/weight/angle that is closest to the middle 500 value 
            # and closest to angle == 0
            if (abs(targetWeight - font.info.weightClass) < abs(targetWeight - font.info.weightClass) or
               abs(targetWidth - font.info.widthClass) < abs(targetWidth - font.info.widthClass) or
               abs(targetAngle - font.info.italicAngle) < abs(targetAngle - font.info.italicAngle)):
               regularFont = font
        return regularFont 
            
  