from pagebot.contexts import defaultContext as context

W = 600
H = 300

HEAD_LINE = """When fonts started a new world"""

TEXT = """The advent of variable fonts means doing nothing, or everything, or something in between for font users and type designers. """

newPage(W, H)

fs = context.newString(HEAD_LINE+'\n',
                       style=dict(font='Verdana',
                                  fontSize=24,
                                  textFill=0))
fs += context.newString(TEXT,
                        style=dict(font='Verdana',
                        fontSize=12,
                        textFill=0))

tw, th = textSize(fs, width=200)
print tw, th
textBox(fs, (100, -th+H, 200, th))
