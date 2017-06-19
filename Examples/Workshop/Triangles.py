path = BezierPath()

# move to a point
path.moveTo((100, 100))
# line to a point
path.lineTo((100, 200))
path.lineTo((200, 200))
# close the path
path.closePath()


# loop over a range of 10
for i in range(20):
    newPage(1000, 1000)
    # set a random color with alpha value of .3
    fill(random(), random(), random(), .3)
    # translate the canvas
    translate(i*35, i*25)
    # in each loop draw the path
    drawPath(path)

saveImage('_export/triangles.gif')