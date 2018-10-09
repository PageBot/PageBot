#!/usr/bin/env python3
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
#     BinaryPDF.py
#
#     Shows how to read and write a PDF file.
#
from pagebot import getContext
import os, os.path

context = getContext()
pdfPath = 'test.pdf'
if not os.path.exists('_export'):
    os.mkdir('_export')

with open(pdfPath, "rb") as binary_file:

    
    # Read the whole file at once
    data = binary_file.read()

    # Copies data.
    newFile = open("_export/testcopy.pdf", "wb")
    newFile.write(data)

    # Shows byte values for first 100 blocks.
    context.newDocument(1100, 1100)
    context.newPage(1100, 1100)
    
    print(len(data))
    x = 100
    y = context.b.height() - 100

    for i in range(101):
        context.text(str(data[i]), (x, y))
        
        x += 100
        if i > 0 and i % 10 == 0:
            x = 100
            y -= 100

    context.saveDocument("_export/bytes.pdf")
