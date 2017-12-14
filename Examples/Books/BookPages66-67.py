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
#     BookPages66-67.py
#
from pagebot.contexts import defaultContext as context

from pagebot.publications.publication import Publication
from pagebot.elements import *
from pagebot.document import Document
from pagebot.conditions import *
from pagebot.style import A5, CENTER, DISPLAY_BLOCK
from pagebot.fonttoolbox.objects.font import Font

h1Style = dict(font='Upgrade-Medium', fontSize=18, rLeading=1.4, tracking=0.2, paragraphBottomSpacing=12*0.5, display=DISPLAY_BLOCK)
h2Style = dict(font='Upgrade-Medium', fontSize=12, rLeading=1.3, tracking=0.2, paragraphTopSpacing=12*1.3*0.5, display=DISPLAY_BLOCK)
bodyStyle = dict(font='Upgrade-Book', fontSize=11, rLeading=1.3, tracking=0.2)
pageNumberStyle = dict(font='Upgrade-Book', fontSize=9, rLeading=1.3, tracking=0.2, xTextAlign=CENTER)
footNoteStyle = dict(font='Upgrade-BookItalic', fontSize=8, rLeading=1.3, tracking=0.2)
footNoteRefStyle = dict(font='Upgrade-Book', fontSize=11, openTypeFeatures=dict(sups=True))

SPECIMEN_TEXT = u"""AÀÁÂÃÄÅĀĂĄǺBCÇĆĈĊČDĎEÈÉÊËĒĔĖĘĚFGĜĞĠĢǦHĤIÌÍÎÏĨĪĬĮİJĴKĶLĹĻĽMNÑŃŅŇOÒÓÔÕÖŌŎŐPQRŔŖŘSŚŜŞŠȘTŢŤȚUÙÚÛÜŨŪŬŮŰŲVWŴẀẂẄXYÝŶŸỲZŹŻŽÆǼÐØǾÞĐĦĿŁŊŒŦΔaàáâãäåāăąǻbcçćĉċčdďeèéêëēĕėęěfgĝğġģǧhĥiìíîïĩīĭįjĵkķlĺļľmnñńņňoòóôõöōŏőpqrŕŗřsśŝşšștţťțuùúûüũūŭůűųvwŵẁẃẅxyýÿŷỳzźżžªºßæǽðøǿ¼½¾₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹_-–—―!"#%&'*,.//:;?@¡·¿†‡•…‰+<=>|~¬±×÷⁄∂∏∑−√∞∫≈≠≤≥^`¨¯´¸˘˙˚˛˜˝¦§©®°¶℗™◊✓Ꞷ₿"""

t = [
    (u"""Design Design Space""", h1Style),
    (u"""is an online coaching environment to develop your design skills. Query your questions and improve your sketching. Acquire new techniques and research your way of presentating. In short, a space where you can design your design process. What kind of challenges do you experience in your daily work as a designer? Working closely together online with experienced designers and a group of other students, there is space to define your own study topics and challenges. In fact, such a selection and planning process is an integral part of the study itself. You tell us what you want, and together we’ll find a way to get there.
""", bodyStyle),
    (u"""Planning""", h2Style),
    (u"""By definition designers are bad planners. It seems to be fundamental to design. Too optimistic in the beginning – “There is still plenty of time”, a design is never finished – “The next one will always be better”.
However, the fact that most designs are supposed to meet external requirements, the final deadline may have a much larger impact on the quality of the result, than the personal opinion of the designer. How do you make this apparent conflict work to your advantage?
""", bodyStyle),
    (u"""How much time do you need?""", h2Style),
    (u"""The core idea behind designing the design process, is that it doesn’t make a difference for how long you do it. A project of 1 hour, basically goes through the same stages (research – design – presentation) as a project of 1 year. Of course, it does matters how long you study something, for the level of details that can be addressed. But if you only have a day or a week for an assignment, then that is part of the requirements. The result can still be better than anything your customer would have done.
How would you design such a design process better next time?
""", bodyStyle),
    (u"""1 day • 1 week • 1 month • 1 season • 1 year""", h2Style),
    (u"""Study lengths range from 1 day, 1 week, 1 month, 1 season and possibly 1 year, whatever fits best to your plans, your practical possibilities and your financial situation.
""", bodyStyle),
    (u"""What is the schedule & how to submit?""", h2Style),
    (u"""Every 6 months, in March and September, a new day-week-month-season-year sequence starts, most likely if there is enough participating students.""", bodyStyle),
    (context.newString(12, style=footNoteRefStyle), None),
    (u""" Day-week sequences or single day Design Games can take place on other dates during the year, if the amount of participants makes it possible. Since working as a team of students a minimum amount of three is required, and also a mininum level of quality, motivation and experience.
Season and year-students are admitted after showing their portfolios and the result of a given assignment. Also they are asked to write a motivation and development plan.
Students that finish a training adequately, automatically get accepted for a next.
""", bodyStyle),
]
specimenText1 = [
    (h2Style['font'], h2Style),
    (SPECIMEN_TEXT, h2Style), 
]
specimenText2 = [
    ('Upgrade-Book', h2Style),
    (SPECIMEN_TEXT, dict(font='Upgrade-Book', fontSize=36, rLeading=1.1, tracking=0.2)), 
]
footNoteText = u"""Repeat to improve: What makes a design process fundamentally different from a production process, is that repetition improves the result. Starting with quick sketches, ignoring most details, next steps take more time. It’s not a linear process, it’s an iterative process, which means repeating the previous step in more detail."""

# Path to markdown file, including Python code blocks.
MD_PATH = u"UsingVariableFonts.md"
# Export path to save the poster PDF.
EXPORT_PATH = '_export/BookPages66-67.pdf'

W, H = A5
M = 48

doc = Document(title='Pages 66-67', w=W, h=H, autoPages=5)

tmp = Template(w=doc.w, h=doc.h, name='DEMO Page', gridY=[(None, 0)], pl=M, pr=M, pt=M, pb=M*1.9)
newTextBox('', parent=tmp, conditions=[Fit2Width(), Fit2Height()], name='Column', h=200)
newText('', parent=tmp, y=H-M, w=112, h=20, conditions=[Center2Center()], name='PageNumber', style=pageNumberStyle)
doc.addTemplate(tmp.name, tmp)
tmp.solve()

cover = Template(w=doc.w, h=doc.h, name='DDS Cover', pl=M, pr=M, pt=M, pb=M*1.5)
newRect(parent=cover, conditions=[Fit2Sides()], name='Background', fill=(0.1, 0.1, 0.5))

# Cover of design space booklet
page = doc[0]
page.applyTemplate(cover)

page = doc[1]
page.applyTemplate(tmp)
page['Column'].setText(context.newText(t))
page['PageNumber'].setText(66)
bs = page['Column'].getOverflow()

page = doc[2]
page.applyTemplate(tmp)
newTextBox('', parent=page, conditions=[Fit2Width(), Bottom2Bottom()], name='FootNotes', h=24)
page.pb = 1.5*M
page['Column'].setText(bs)
page['Column'].append(context.newText(specimenText1))
page['PageNumber'].setText(67)
footNote = context.newString(12, style=footNoteRefStyle) + context.newString(' '+footNoteText, style=footNoteStyle)
page['FootNotes'].setText(footNote, style=footNoteStyle)

page = doc[3]
page.applyTemplate(tmp)
newTextBox('', parent=page, conditions=[Fit2Width(), Bottom2Bottom()], name='FootNotes', h=48)
page['Column'].setText(context.newText(specimenText2))
page['PageNumber'].setText(68)
bs = page['Column'].getOverflow()

page = doc[4]
page.applyTemplate(tmp)
newTextBox('', parent=page, conditions=[Fit2Width(), Bottom2Bottom()], name='FootNotes', h=48)
page['Column'].setText(bs)
page['PageNumber'].setText(69)

# Views define the way documents are exported.
# Add space for cropmarks and registrations marks
view = doc.getView()
view.padding = 0
view.showPageNameInfo = True
view.showPagePadding = False # No need, as we are drawing the grid
view.showPageCropMarks = True
view.showPageRegistrationMarks = True
view.showPageFrame = True 
view.showGrid = False

view.style['viewGridStroke'] = (0, 0, 1)
view.style['viewGridStrokeWidth'] = 0.5

doc.solve()

doc.export(EXPORT_PATH)