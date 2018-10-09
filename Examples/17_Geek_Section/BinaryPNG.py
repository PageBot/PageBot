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
#     BinaryPNG.py
#
#     Shows how to read and write a PNG image as a binary file.
#

from pagebot import getContext
from pagebot import getResourcesPath
import os, os.path

context = getContext()
imagePath = getResourcesPath() + "/images/peppertom_lowres_398x530.png"

with open(imagePath, "rb") as binary_file:

    
    # Read the whole file at once
    data = binary_file.read()
    #mutable_bytes = bytearray(data)
    #print(len(mutable_bytes))
    if not os.path.exists('_export'):
        os.mkdir('_export')
    newFile = open("_export/test.png", "wb")
    newFile.write(data)

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

    # TODO: Close and save drawing?

    binary_file.seek(0, 2)  # Seek the end
    num_bytes = binary_file.tell()  # Get the file size

    count = 0
    
    for i in range(num_bytes):
        binary_file.seek(i)
        eight_bytes = binary_file.read(8)
        
        if eight_bytes == b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a":  # PNG signature
            count += 1
            print("Found PNG Signature #" + str(count) + " at " + str(i))
            
            # Next four bytes after signature is the IHDR with the length
            png_size_bytes = binary_file.read(4)
            png_size = int.from_bytes(png_size_bytes, byteorder='little', signed=False)

            # Go back to beginning of image file and extract full thing
            binary_file.seek(i)
            # Read the size of image plus the signature
            #png_data = binary_file.read(png_size + 8)
            #with open("pngs/" + str(i) + ".png", "wb") as outfile:
            #    outfile.write(png_data)

    # Seek position and read N bytes
    #binary_file.seek(0)  # Go to beginning
    #couple_bytes = binary_file.read(2)
    #print(couple_bytes)
