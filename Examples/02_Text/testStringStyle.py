
TEMPLATE_NAME = 'One-More_B-o-B_TYPE-3_Layout-01_rb.pdf'

indent = pt(15)
tabs = [(indent, LEFT)]

print(titleBold, bookFont, bitcountPropSingle)

style1 = dict(font=titleBold, fontSize=30, textFill=color('red'), xTextAlign=LEFT)
style1a = dict(font=bookFont, fontSize=16.40,xTextAlign=LEFT)
style1b = dict(font=bitcountPropSingle, fontSize=15, xTextAlign=LEFT)

style2 = dict(font=bodyText, fontSize=10, leading=em(1.4))
style3 = dict(font=titleBold, fontSize=14, tabs=tabs, leading=em(1.1))
style4 = dict(font=bodyText, fontSize=10, leading=em(1.2), tabs=tabs, firstLineIndent=0, indent=indent)
style4a = dict(font=bodyText, fontSize=10, leading=em(1.2), tabs=tabs, firstLineIndent=0, indent=indent, tracking=em(0.05))
style5 = dict(font=bodyText, fontSize=10, leading=em(1.7), tabs=tabs, firstLineIndent=0, indent=indent)
# Issue number style for path
style8 = dict(font=titleBold, fontSize=180)

h1 = 'ONE MORE THING\n'
h2 = 'Length matters\n'
h3 = 'Some rules for readability'


context = getContext()

doc = Document(w=1000, h=1000, originTop=False, context=context)
page = doc[1]
bs = context.newString(h1, style=style1b)
bs += context.newString(h2, style=style1)
bs += context.newString(h3, style=style1a)
newTextBox(bs, parent=page, h=140, conditions=(Top2Top(), Fit2Width()), fill=(0.9, 0.9, 0.9, 0.9))


doc.exportPages('')