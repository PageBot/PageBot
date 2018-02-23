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
#     publications.py
#
from pagebot.contexts import defaultContext as context
from pagebot.fonttoolbox.objects.font import getFontByName
from pagebot.style import A5, CENTER, DISPLAY_BLOCK, RIGHT, LEFT
from pagebot.fonttoolbox.objects.family import findFamilyByName
# Try to find if the TYPETR Upgrade family is installed, Otherwise use PageBot installed Roboto instead.
# TYPETR Upgrade can be viewed here: https://upgrade.typenetwork.com
# And licensed here: https://store.typenetwork.com/foundry/typetr/series/upgrade
family = findFamilyByName('Upgrade')
if family is None: # Upgrade not available, use Google's Roboto instead.
    family = findFamilyByName('Roboto')
print family

h1Style = dict(font='Upgrade-Medium', fontSize=13, rLeading=1.4, tracking=0.2, paragraphBottomSpacing=13, display=DISPLAY_BLOCK)
h2Style = dict(font='Upgrade-Medium', fontSize=11, rLeading=1.3, tracking=0.2, paragraphTopSpacing=12*1.3*0.5, display=DISPLAY_BLOCK)
bodyStyle = dict(font='Upgrade-Book', fontSize=10, rLeading=1.3, tracking=0.2)
pageNumberStyle = dict(font='Upgrade-Book', fontSize=9, rLeading=1.3, tracking=0.2, xTextAlign=CENTER)
footNoteStyle = dict(font='Upgrade-BookItalic', fontSize=8, rLeading=1.3, tracking=0.2)
footNoteRefStyle = dict(font='Upgrade-Book', fontSize=10, openTypeFeatures=dict(smcp=True))
pageChapterStyle = dict(font='Upgrade-BookItalic', fontSize=8, rLeading=1.3, tracking=0.2, xTextAlign=RIGHT)
pageTitleStyle = dict(font='Upgrade-BookItalic', fontSize=8, rLeading=1.3, tracking=0.2, xTextAlign=LEFT)

footNoteRef = 12

bookTitle = 'Design: Educating the process'
chapterTitle = 'Design Design Space'
t = [
    (chapterTitle, h1Style),
    (u"""is an online coaching environment to develop your design skills. Query your questions and improve your sketching. Acquire new techniques and research your way of presentating. In short, a space where you can design your design process. What kind of challenges do you experience in your daily work as a designer? Working closely together online with experienced designers and a group of other students, there is space to define your own study topics and challenges. In fact, such a selection and planning process is an integral part of the study itself. You tell us what you want, and together we’ll find a way to get there.
""", bodyStyle),
    (u"""Planning""", h2Style),
    (u"""By definition designers are bad planners. It seems to be fundamental to design. Too optimistic in the beginning – “There is still plenty of time”, a design is never finished – “The next one will always be better”.
However, the fact that most designs are supposed to meet external requirements, the final deadline may have a much larger impact on the quality of the result, than the personal opinion of the designer. How do you make this apparent conflict work to your advantage?
""", bodyStyle),
    (u"""How much time do you need?""", h2Style),
    (u"""The core idea behind designing the design process, is that it doesn’t make a difference for how long you do it. A project of 1 hour, basically goes through the same stages (research – design – presentation) as a project of 1 year. Of course, it does matters how long you study something, for the level of details that can be addressed. But if you only have a day or a week for an assignment, then that is part of the requirements.""", bodyStyle),
    (context.newString(footNoteRef, style=footNoteRefStyle), None),
    (u""" The result can still be better than anything your customer would have done.
How would you design such a design process better next time?
""", bodyStyle),
    (u"""1 day • 1 week • 1 month • 1 season • 1 year""", h2Style),
    (u"""Study lengths range from 1 day, 1 week, 1 month, 1 season and possibly 1 year, whatever fits best to your plans, your practical possibilities and your financial situation.
""", bodyStyle),
    (u"""What is the schedule & how to submit?""", h2Style),
    (u"""Every 6 months, in March and September, a new day-week-month-season-year sequence starts, most likely if there is enough participating students.""", bodyStyle),
    (u""" Day-week sequences or single day Design Games can take place on other dates during the year, if the amount of participants makes it possible. Since working as a team of students a minimum amount of three is required, and also a mininum level of quality, motivation and experience.
Season and year-students are admitted after showing their portfolios and the result of a given assignment. Also they are asked to write a motivation and development plan.
Students that finish a training adequately, automatically get accepted for a next.
""", bodyStyle),
]
footNoteText = u"""Repeat to improve: What makes a design process fundamentally different from a production process, is that repetition improves the result. Starting with quick sketches, ignoring most details, next steps take more time. It’s not a linear process, it’s an iterative process, which means repeating the previous step in more detail."""

M = 65
ML, MR, MT, MB = M, 0.75*M, M, 1.5*M

def buildDesignPages(w, h):

    cw = w-ML-MR
    
    # Page 66
    context.newPage(w, h) 
    bs = context.newText(t)

    R = (ML, MB, w-ML-MR, h-MB-MT)
    overFill = context.textOverflow(bs, R)
    context.textBox(bs, R)

    pn = context.newString(66, style=pageNumberStyle)
    context.text(pn, (w/2 - pn.w/2, M/2))

    pt = context.newString(bookTitle, style=pageTitleStyle)
    context.textBox(pt, (ML, h-MT*0.75, cw, pt.h))

    # Page 67
    context.newPage(w, h) 
    # Assume that we have a footnote on this page, calc it's space.
    fnMark = context.newString(footNoteRef, style=footNoteRefStyle)
    fn = fnMark + ' ' + context.newString(footNoteText, style=footNoteStyle)
    fnw, fnh = fn.textSize(cw)
    cfnh = fnh+bodyStyle['fontSize']*bodyStyle['rLeading']
    ch = h-MB-MT-cfnh
    R = (ML, MB+cfnh, cw, ch)
    context.textBox(overFill, R)

    context.textBox(fn, (ML, MB, cw, fnh))

    pt = context.newString(chapterTitle, style=pageChapterStyle)
    context.textBox(pt, (ML, h-MT*0.75, cw, pt.h))
    
    pn = context.newString(67, style=pageNumberStyle)
    context.text(pn, (w/2 - pn.w/2, M/2))


IMAGES = (
    ('designPages.png', 350, 500, buildDesignPages),)        
      
for path, w, h, m in IMAGES:
    newDrawing()
    m(w, h)
    imagePath = '_export/'+path
    saveImage(imagePath, multipage=True)
    print imagePath
    