# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     TestDrawVariables.py
#
# create small ui element for variables in the script

if __name__ == '__main__':

    Variable([
        # create a variable called 'w'
        # and the related ui is a Slider.
        dict(name="w", ui="Slider"),
        # create a variable called 'h'
        # and the related ui is a Slider.
        dict(name="h", ui="Slider",
                args=dict(
                    # some vanilla specific
                    # setting for a slider
                    value=100,
                    minValue=50,
                    maxValue=300)),
        # position of the rectangle
        dict(name="x", ui="Slider",
            args=dict(value=0, minValue=0, maxValue=1000)),
        dict(name="y", ui="Slider",
            args=dict(value=0, minValue=0, maxValue=1000)),
        # create a variable called 'useColor'
        # and the related ui is a CheckBox.
        dict(name="useColor", ui="CheckBox"),
        # create a variable called 'c'
        # and the related ui is a ColorWell.
        dict(name="c", ui="ColorWell")
        ], globals())

    # check if the 'useColor' variable is checked
    if useColor:
        # set the fill color from the variables
        fill(c)
    # draw a rect
    rect(x, y, w, h)
    # set the font size
    fontSize(h)
    # draw some text
    text("Hello Variable", (w, h))
