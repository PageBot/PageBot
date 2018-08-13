# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     classHierarchy.py
#
import pagebot
import pagebot.contexts.drawbotcontext
import sys, inspect

def drawClassHierarchy(obj):
    x = 100
    y = 100
    for c in obj.__mro__:
        drawClass(c, x, y)
        y += 100
    print('...')

def drawClass(c, x, y):
    print(c)
    
classes = inspect.getmembers(sys.modules['pagebot.contexts.drawbotcontext'])

for name, obj in classes:
    if inspect.isclass(obj):
        drawClassHierarchy(obj)
        
