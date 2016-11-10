import collections
import itertools


# Utility function for distance eval
def dist(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


Line = collections.namedtuple('Line', ['a', 'b', 'c'])
Point = collections.namedtuple('Point', ['x', 'y'])


def dist2line(pt, line):
    pt = Point._make(pt)
    line = Line._make(line)
    return abs((line.a*pt.x + line.b*pt.y + line.c) /
               ((line.a**2 + line.b**2)**0.5))


def calcline(p1, p2):
    p1 = Point._make(p1)
    p2 = Point._make(p2)

    a = p2.y - p1.y
    b = p1.x - p2.x
    c = p2.x * p1.y - p2.y * p1.x

    return Line._make((a, b, c))

class Hierarchy:
    def __init__(self, hrki):
        self.hierarchy = hrki

    def tour(self, node, layer=0, visual=False):
        def p(text):
            print '%s%s' % ('\t' * layer, text)

        p = p if visual else lambda x: None

        while True:
            p('> %s' % node)
            yield node, layer

            # tour child
            if self.hierarchy[node][2] >= 0:
                for subnode in self.tour(self.hierarchy[node][2], layer + 1, visual):
                    yield subnode

            # if no next
            if self.hierarchy[node][0] >= 0:
                node = self.hierarchy[node][0]
            else:
                break

        p('<')

    def spot(self, node, visual=False):
        childidx = self.hierarchy[node][2]
        if childidx < 0:
            return

        for ni in self.tour(childidx, visual=visual):
            yield ni

    def delete_node(self, idx):
        node = self.hierarchy[idx]
        nexti = node[0]
        previ = node[1]
        childi = node[2]
        parenti = node[3]

        parent = self.hierarchy[parenti]
        fchild = self.hierarchy[childi]

        if childi >= 0:
            last_childi = childi
            while self.hierarchy[last_childi][0] >= 0:
                last_childi = self.hierarchy[last_childi][0]

            if nexti >= 0:
                self.hierarchy[nexti][1] = last_childi
                self.hierarchy[last_childi][0] = nexti
            if previ >= 0:
                self.hierarchy[previ][0] = childi

            if parent[2] == idx:
                parent[2] = childi

        else:
            if nexti >= 0:
                self.hierarchy[nexti][1] = previ
            if previ >= 0:
                self.hierarchy[previ][0] = nexti

            if parent[2] == idx:
                parent[2] = nexti

                # f = open('output', 'a')
                # f.write(str(self.hierarchy))
                # f.write('$')
                # f.close()

    # delete_node = lambda *args: None

    def copy(self):
        return Hierarchy(list(self.hierarchy))

colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255)
]

icolor = itertools.cycle(colors)
