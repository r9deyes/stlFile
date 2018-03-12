class Triangle:
    v1, v2, v3 = None, None, None
    n = (0.0, 0.0, 0.0)

    def __init__(self, v1x, v1y, v1z,
                 v2x=None, v2y=None, v2z=None,
                 v3x=None, v3y=None, v3z=None,
                 n=(0.0, 0.0, 0.0)):
        if ((isinstance(v1x, tuple) or isinstance(v1x, list))
        and (isinstance(v1y, tuple) or isinstance(v1y, list))
        and (isinstance(v1z, tuple) or isinstance(v1z, list))):
            self.v1 = (float(v1x[0]), float(v1x[1]), float(v1x[2]))
            self.v2 = (float(v1y[0]), float(v1y[1]), float(v1y[2]))
            self.v3 = (float(v1z[0]), float(v1z[1]), float(v1z[2]))
        else:
            self.v1 = (float(v1x), float(v1y), float(v1z))
            self.v2 = (float(v2x), float(v2y), float(v2z))
            self.v3 = (float(v3x), float(v3y), float(v3z))
        self.n = n


class StlFile:
    name = None
    triangles = []

    def __init__(self, name):
        self.name = name

    def add_triangle(self, v1, v2, v3, normal=(0.0, 0.0, 0.0)):
        self.triangles.append(Triangle(v1, v2, v3, n=normal))

    def open(self, fileName):
        f = open(fileName, 'r')
        t = None
        solid = None
        res = []
        for s in f:
            if s[:7] == 'vertex ':
                t.append(s[7:].split())
                continue
            if s[:6] == 'solid ':
                solid = StlFile(s[6:])
                continue
            if s[:13] == 'facet normal ':
                t = [s[13:].split()]
                continue
            if s[:10] == 'outer loop':
                continue
            if s[:7] == 'endloop':
                solid.add_triangle(t[1], t[2], t[3], normal=t[0])
                continue
            if s[:9] == 'endsolid ':
                if s[9:] == solid.name:
                    res.append(solid)
                    solid = None
                continue
        f.close()
        return res

    def save(self, fileName, filePermision = 'w'):
        f = open(fileName, filePermision)
        f.write('solid %s\n' % self.name)
        for t in self.triangles:
            f.write('facet normal %f %f %f\n' % (t.n[0], t.n[1], t.n[2]))
            f.write('outer loop\n')
            f.write('vertex %f %f %f\n' % (t.v2[0], t.v2[1], t.v2[2]))
            f.write('vertex %f %f %f\n' % (t.v3[0], t.v3[1], t.v3[2]))
            f.write('vertex %f %f %f\n' % (t.v1[0], t.v1[1], t.v1[2]))
            f.write('endloop\nendfacet\n')
        f.write('endsolid %s\n'%self.name)
        f.close()

    def rotate(self, angle, axes):
        for t in self.triangles:
            t.v1 = rotate(t.v1, angle, axes)
            t.v2 = rotate(t.v2, angle, axes)
            t.v3 = rotate(t.v3, angle, axes)
            t.n = rotate(t.n, angle, axes)

    def scale(self, coef, axes):
        for t in self.triangles:
            t.v1 = scale(t.v1, coef, axes)
            t.v2 = scale(t.v2, coef, axes)
            t.v3 = scale(t.v3, coef, axes)

    def move(self, distance, axes):
        for t in self.triangles:
            t.v1 = move(t.v1, distance, axes)
            t.v2 = move(t.v2, distance, axes)
            t.v3 = move(t.v3, distance, axes)


def rotation_matrix(theta, axe='x'):
    from math import cos, sin
    theta = float(theta/57.2958)
    c, s = float(cos(theta)), float(sin(theta))
    if axe == 'z':
        R =		[[c, -s,0.0,0.0],
                [s, c,0.0,0.0],
                [0.0,0.0,1.0,0.0],
                [0.0,0.0,0.0,1.0]]
    elif axe == 'x':
        R =		[[1.0, 0.0, 0.0, 0.0],
                [0.0, c, s, 0.0],
                [0.0, -s, c, 0.0 ],
                [0.0, 0.0, 0.0, 1.0]]
    elif axe == 'y':
        R =		[[c, 0.0, s, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [-s, 0.0, c, 0.0],
                [0.0, 0.0, 0.0, 1.0]]
    return R

def matrix_multiplication(m, v):
    return (m[0][0] * v[0] + m[0][1] * v[1] + m[0][2] * v[2] + m[0][3] * v[3],
            m[1][0] * v[0] + m[1][1] * v[1] + m[1][2] * v[2] + m[1][3] * v[3],
            m[2][0] * v[0] + m[2][1] * v[1] + m[2][2] * v[2] + m[2][3] * v[3])

def rotate(vertex, angle, axes='x'):
    res = list(vertex)
    for axe in axes:
        v = list(res) + [1.0]
        m = rotation_matrix(angle, axe=axe)
        res = matrix_multiplication(m, v)
    return res

def scale(vertex, coef, axes='x'):
    res = list(vertex)
    if axes.find('x')+1:
        res[0] *= coef
    if axes.find('y')+1:
        res[1] *= coef
    if axes.find('z')+1:
        res[2] *= coef
    return res

def move(vertex, distance, axes='x'):
    res = list(vertex)
    if axes.find('x')+1:
        res[0] += distance
    if axes.find('y')+1:
        res[1] += distance
    if axes.find('z')+1:
        res[2] += distance
    return res

def triangle():
    c = StlFile('triangle')
    c.add_triangle((0.667, 0.0, 0.0),
            (-0.667, 0.667, 0.0),
            (-0.667, -0.667, 0.0),
            (0.0, 0.0, 1.0))
    return c
def plane():
    c = StlFile('plane')
    c.add_triangle((1.0, 1.0, 0.0),
                   (-1.0, 1.0, 0.0),
                   (1.0, -1.0, 0.0),
                   (0.0, 0.0, 1.0))
    c.add_triangle((-1.0, -1.0, 0.0),
                   (1.0, -1.0, 0.0),
                   (-1.0, 1.0, 0.0),
                   (0.0, 0.0, 1.0))
    return c

def square():
    c = StlFile('square')
    c.add_triangle((1.0, 1.0, 0.0),
                   (0.0, 0.0, 0.0),
                   (-1.0, 1.0, 0.0),
                   (0.0, 0.0, 1.0))
    c.add_triangle((-1.0, 1.0, 0.0),
                   (0.0, 0.0, 0.0),
                   (-1.0, -1.0, 0.0),
                   (0.0, 0.0, 1.0))
    c.add_triangle((-1.0, -1.0, 0.0),
                   (0.0, 0.0, 0.0),
                   (1.0, -1.0, 0.0),
                   (0.0, 0.0, 1.0))
    c.add_triangle((1.0, -1.0, 0.0),
                   (0.0, 0.0, 0.0),
                   (1.0, 1.0, 0.0),
                   (0.0, 0.0, 1.0))
    return c

def sphere(edgeCount=16):
    from math import cos, sin, pi
    c = StlFile('sphere')
    #x0 = cos(2*pi / edgeCount)
    #y0 = sin(2*pi / edgeCount)
    x0, y0 = 1.0, 0.0
    a0, b0 = 0.0, 0.0
    z0 = -1.0
    preCircleX=[0.0]*edgeCount
    preCircleY=[0.0]*edgeCount
    for j in range(edgeCount+1):
        size = 1 - edgeCount / abs(j-edgeCount/2)
        z = cos(2*pi/ edgeCount * j)
        for i in range(edgeCount+1):
            x = cos(2 * pi / edgeCount * i)
            y = sin(2 * pi / edgeCount * i)

            if j == 0:
                c.add_triangle((0.0, 0.0, z0),
                               (x, y, z),
                               (x0, y0, z),
                               normal=(x, y, z))
            elif j == edgeCount:
                z0 = 1.0
                c.add_triangle((0.0, 0.0, z0),
                               (x, y, z),
                               (x0, y0, z),
                               normal=(x, y, z))
            else:
                a = cos(2*pi / edgeCount * (i+1))
                b = sin(2*pi / edgeCount * (i+1))
                c.add_triangle((a, b, z0),
                               (x, y, z),
                               (x0, y0, z),
                               normal=(x, y, z))
                c.add_triangle((a, b, z0),
                               (a0, a0, z0),
                               (x, y, z),
                               normal=(x, y, z))

            x0, y0 = x, y
            a0, b0 = a, b
        z0 = z
    return c

def cylinder(edgeCount=16):
    from math import cos, sin, pi
    c=StlFile('cylinder')
    x0, y0 = 1.0, 0.0
    for i in range(edgeCount):
        x = cos(pi / edgeCount*(1+i)*2)
        y = sin(pi / edgeCount*(1+i)*2)
        c.add_triangle((0.0, 0.0, -1.0),
                       (x, y, -1.0),
                       (x0, y0, -1.0),
                       normal=(0.0, 0.0, -1.0))
        c.add_triangle((0.0, 0.0, 1.0),
                       (x, y, 1.0),
                       (x0, y0, 1.0),
                       normal=(0.0, 0.0, 1.0))
        c.add_triangle((x0, y0, 1.0),
                       (x, y, -1.0),
                       (x0, y0, -1.0),
                       normal=(x, y, -1.0))
        c.add_triangle((x0, y0, 1.0),
                       (x, y, 1.0),
                       (x, y, -1.0),
                       normal=(x, y, 0.0))
        x0, y0 = x, y
    return c

def nurb():
    return StlFile('nurb')


if __name__ == '__main__':
    c = cylinder()
    c.save('D:/Users/DAN85_000/Desktop/1a.stl')
    c.move(17.0, 'x')
    c.save('D:/Users/DAN85_000/Desktop/1b.stl')
    c.rotate(30.0,'yz')
    c.save('D:/Users/DAN85_000/Desktop/1c.stl')
    c.scale(5,'x')
    c.save('D:/Users/DAN85_000/Desktop/1d.stl')