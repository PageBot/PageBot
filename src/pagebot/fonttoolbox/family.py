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
        self.styles = {}

    def __len__(self):
        return len(self.styles)
        
    def addStyle(self, style):
        assert not style.styleName in self.styles
        self.styles[style.styleName] = style
        
    def getRegularStyle(self):
        # Answer the style that has width/weight closest to 500 and angle is closest to 0
        targetWeight = targetWidth = 500
        targetAngle = 0
        regularStyle = None
        for style in self.styles.values():
            if regularStyle is None: # Take the first to compare with.
                regularStyle = style
                continue
            # Find style that has width/weight/angle that is closest to the middle 500 value 
            # and closest to angle == 0
            if (abs(targetWeight - style.info.weightClass) < abs(targetWeight - regularStyle.info.weightClass) or
               abs(targetWidth - style.info.widthClass) < abs(targetWidth - regularStyle.info.widthClass) or
               abs(targetAngle - style.info.italicAngle) < abs(targetAngle - regularStyle.info.italicAngle)):
               regularStyle = style
        return regularStyle 
            
  