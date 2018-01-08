from pagebot.contexts import defaultContext as context

W = 600
H = 300

HEAD_LINE = """When fonts started a new world"""

TEXT = """The advent of variable fonts means doing nothing, or everything, or something in between for font users and type designers. """

newPage(W, H)

bs = context.newString(HEAD_LINE+'\n',
                       style=dict(font='Verdana',
                                  fontSize=24,
                                  textFill=0))
bs += context.newString(TEXT,
                        style=dict(font='Verdana',
                        fontSize=12,
                        textFill=0))

tw, th = context.textSize(bs, w=200)
print tw, th
context.textBox(bs, (100, -th+H, 200, th))
