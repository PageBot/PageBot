from pagebot.gxtools.gxmutator import generateInstance

"""
location = {
	"wght": 0.765,
	"wdth": -0.43,
}

generateInstance('Promise-GX.ttf', location, targetDirectory="instances")
"""

locations = [
    dict(wght=0.765, wdth=-0.430),
    dict(wght=0.100, wdth=0.900),
    ]
    
for location in locations:
    generateInstance('../fonts/Promise-GX.ttf', location, targetDirectory="../fonts/instances")
