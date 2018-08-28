
import math


def _dotProduct(array, matrix):
    output = []
    for pt in array:
        if not output:
            assert len(pt) == len(matrix) == len(matrix[0])
        outPt = []
        for i in range(len(pt)):
            t = 0
            for j, c in enumerate(pt):
                t += c * matrix[j][i]
            outPt.append(t)
        output.append(tuple(outPt))
    return tuple(output)


def _offsetArray3D(array, offset):
    dx, dy, dz = offset
    for x, y, z in array:
        yield x+dx, y+dy, z+dz


class Transform3D:

    def __init__(self, matrix=None, offset=None):
        if matrix is None:
            matrix = ((1.0, 0.0, 0.0),
                      (0.0, 1.0, 0.0),
                      (0.0, 0.0, 1.0))
        if offset is None:
            offset = [0, 0, 0]
        self.matrix = matrix
        self.offset = offset

    def translate(self, dx, dy, dz):
        return self.transform(None, (dx, dy, dz))

    def scale(self, xScale=1.0, yScale=None, zScale=None):
        if yScale is None:
            yScale = xScale
        if zScale is None:
            zScale = yScale
        matrix = ((xScale, 0, 0), (0, yScale, 0), (0, 0, zScale))
        return self.transform(matrix)

    def rotateX(self, angle):
        s = math.sin(angle)
        c = math.cos(angle)
        return self.transform(((1, 0, 0), (0, c, -s), (0, s, c)))

    def rotateY(self, angle):
        s = math.sin(angle)
        c = math.cos(angle)
        return self.transform(((c, 0, s), (0, 1, 0), (-s, 0, c)))

    def rotateZ(self, angle):
        s = math.sin(angle)
        c = math.cos(angle)
        return self.transform(((c, -s, 0), (s, c, 0), (0, 0, 1)))

    def transform(self, other=None, offset=None):
        if isinstance(other, Transform3D):
            assert offset is None
            other, offset = other.matrix, other.offset
        x, y, z = self.offset
        if offset is not None:
            dx, dy, dz = _dotProduct([offset], self.matrix)[0]
            x += dx
            y += dy
            z += dz
        if other:
            matrix = _dotProduct(other, self.matrix)
        else:
            matrix = self.matrix
        return self.__class__(matrix, (x, y, z))

    def transformPoint(self, pt):
        return self.transformPoints([pt])[0]

    def transformPoints(self, points):
        points = _dotProduct(points, self.matrix)
        if self.offset != (0, 0, 0):
            points = list(_offsetArray3D(points, self.offset))
        return points

    def getAffineTransform2D(self, axis=1):
        matrix = self.matrix
        dx, dy, dz = self.offset
        if axis == 1:
            xi = 0
            yi = 2
        elif axis == 2:
            xi = 0
            yi = 1
        else:
            raise NotImplementedError()
        affine = [matrix[xi][xi], matrix[xi][yi], matrix[yi][xi], matrix[yi][yi], self.offset[xi], self.offset[yi]]
        return affine

    # def __len__(self):
    #     return len(self.matrix)

    # def __getitem__(self, index):
    #     return self.matrix[index]

    # def __iter__(self):
    #     return iter(self.matrix)

    def __repr__(self):
        return "<%s %s %s>" % (self.__class__.__name__, self.matrix, self.offset)


if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

