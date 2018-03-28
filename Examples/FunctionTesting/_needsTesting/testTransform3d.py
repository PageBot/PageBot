from pagebot import getResourcesPath
from pagebot.toolbox.transform3d import Transform3D

def circle(cpt, r):
    cx, cy = cpt
    d = r * 2
    oval(cx - r, cy - r, d, d)


translate(width()/2, height()/2)

t = Transform3D()  # identity transform

print(t.transformPoint((100, 200, 300))  # transform one point)
print(t.transformPoints([(100, 200, 300)])  # transform a seq. of points)

print(t)

radius = 222
cube = []
for x in [-radius, radius]:
    for y in [-radius, radius]:
        for z in [-radius, radius]:
            cube.append((x, y, z))

t = Transform3D()  # identity transform
t = t.rotateX(radians(68))
t = t.rotateY(radians(8))
t = t.rotateZ(radians(--10))

affine = t.getAffineTransform2D(2)

imagePath = getResourcesPath() + "/images/peppertom_lowres_398x530.png"
w, h = imageSize(imagePath)

fontSize(40)
for x, y, z in sorted(t.transformPoints(cube), key=lambda pt: pt[2]):
    save()
    translate(x, y)
    transform(affine)
    scale(0.15)
    # fill(1 - (z / 300 + 0.5))
    circle((0, 0), 50)
    # text("R", (0, 0))
    image(imagePath, (-w/2, -h/2))
    restore()
