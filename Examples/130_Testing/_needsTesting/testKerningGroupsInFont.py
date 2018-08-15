from pagebot.fonttoolbox.objects.font import Font
from pagebot.contributions.adobe.kerndump.getKerningPairsFromOTF import OTFKernReader

f = Font(u"/Library/Fonts/Upgrade-Medium.otf")

print(len(f.kerning))

#print(OTFKernReader(f.path).kerningPairs)
okr = OTFKernReader(f.path)
okr.getClassPairs()
okr.getSinglePairs()
print(okr.classPairs)
#print(okr.singlePairs)
#print(okr.pairPosList)

