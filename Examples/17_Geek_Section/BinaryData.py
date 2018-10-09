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
#     BinaryData.py
#
#     Shows how to read and write binary data. More here:
#
#     https://www.devdungeon.com/content/working-binary-data-python


# Creates empty bytes.
empty_bytes = bytes(4)
print(type(empty_bytes))
print(empty_bytes)

# Casts bytes to bytearray.
mutable_bytes = bytearray(empty_bytes)
print(mutable_bytes)
mutable_bytes = bytearray(b'\x00\x0F')

# Bytearray allows modification:
mutable_bytes[0] = 255
mutable_bytes.append(255)
print(mutable_bytes)

# Cast bytearray back to bytes
immutable_bytes = bytes(mutable_bytes)
print(immutable_bytes)

s = b'bla'
print(s.decode('utf8'))
