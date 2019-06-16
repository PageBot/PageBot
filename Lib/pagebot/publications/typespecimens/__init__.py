# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     __init__.py
#
#     If we revive type from the past, why not type specimens of the past?
#     Take an old book from the shelf, measure the relevant parameters
#     and design their relational algorythms.
#     The TypeSpecimen class (or other lists on this default page) may be 
#     a starting point of thinking or even can be used as class to inherit from.
#     More revivals will be added over time.
#     And more new types of type speciimens will be developed as well.
#
from pagebot.publications.typespecimens.typespecimen import TypeSpecimen
from pagebot.publications.typespecimens.simplespecimen import SimpleSpecimen
#from pagebot.publications.typespecimens.fontographer35keymap import Fontographer35KeyMap

TYPE_SPECIMEN_CLASSES = {
	'Standard': TypeSpecimen,
    'Simple': SimpleSpecimen,
#    'Fog35': Fontographer35KeyMap,
}