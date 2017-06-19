
size(400, 400)
# x, y, w, h
for n in range(642):
    fill(random(), random(), random(), 0.5)
    x = random()*400
    y = random()*392
    if random()<0.5:
        rect(x, y, random()*14+10, 36)
    else:
        oval(x, y, random()*14+10, 16)

print random()