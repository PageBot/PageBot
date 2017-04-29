

"""

GS = 1.61803398874989484820

font('Verdana')
fontSize(12)

s = S = 250
v = V = 40
stroke(1, 0, 0)
fill(None)

for n in range(3):
    stroke(0)
    rect(400-s/2, 400-s/2, s, s)

    fill(0)
    stroke(None)
    text('%0.2f' % (s/S*100), (400-s/2, 400-s/2))
    fill(None)

    v = v*GS
    s += v
      
s = S 
v = V
for n in range(3):
    stroke(0)
    rect(400-s/2, 400-s/2, s, s)
    
    fill(0)
    stroke(None)
    text('%0.2f' % (s/S*100), (400-s/2, 400-s/2))
    fill(None)
    
    v = v/GS
    s -= v
"""

D = 14
data = (
    (52, D),
    (76, D),
    (100, D),
    (124, D),
    (126, D),
    )
s = 3
V = 44
for n in range(5):
    #d = D
    w, d = data[n]
    print V-d, V, V+d
    sv = s*V
    V += d*2
    d *= s
    fill(None)
    stroke(0)
    rect(500-sv/2, 500-sv/2, sv, sv)
    stroke(1, 0, 0)
    rect(500-sv/2+d/2, 500-sv/2+d/2, sv-d, sv-d)
    stroke(0, 1, 0)
    rect(500-sv/2-d/2-1, 500-sv/2-d/2-1, sv+d+2, sv+d+2)
    