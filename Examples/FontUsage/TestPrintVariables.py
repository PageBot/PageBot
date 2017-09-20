
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     TestPrintVariables.py
#
# Variable == vanilla power in DrawBot
from AppKit import NSColor

if __name__ == '__main__':

	# create a color
	_color = NSColor.colorWithCalibratedRed_green_blue_alpha_(0, .5, 1, .8)
	# setup variables useing different vanilla ui elements.
	Variable([
	    dict(name="aList", ui="PopUpButton", args=dict(items=['a', 'b', 'c', 'd'])),
	    dict(name="aText", ui="EditText", args=dict(text='hello world')),
	    dict(name="aSlider", ui="Slider", args=dict(value=100, minValue=50, maxValue=300)),
	    dict(name="aCheckBox", ui="CheckBox", args=dict(value=True)),
	    dict(name="aColorWell", ui="ColorWell", args=dict(color=_color)),
	    dict(name="aRadioGroup", ui="RadioGroup", args=dict(titles=['I', 'II', 'III'], isVertical=False)),
	], globals())

	print aList
	print aText
	print aSlider
	print aCheckBox
	print aColorWell
	print aRadioGroup
