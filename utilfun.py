import collections
import itertools
import cv2
import numpy as np


# Utility function for distance eval
def dist(p, q):
    return ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) ** 1/2


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


def drawContour(img, contour):
    return cv2.drawContours(img, [contour], 0, icolor.next())


def imshow(img):
    cv2.imshow('show', img)
    cv2.waitKey(0)


def polygonFit(contour, factor=0.05):
    # type: (object, float) -> np.ndarray
    eps = factor * len(contour)
    return cv2.approxPolyDP(contour, eps, closed=True)


def resize2(img, expected_width):
    height, width = img.shape

    factor = float(width) / expected_width
    img = cv2.resize(img, dsize=(expected_width, int(height / factor)),
                     interpolation=cv2.INTER_LINEAR)

    return img


def calc_rect_points(bounding_rect):
    x, y, w, h = bounding_rect
    points = [
        (x, y),
        (x + w, y),
        (x + w, y + h),
        (x, y + h)
    ]
    return points


def direction_arrow_gen(dir, size):
    # type: (str, int) -> (Point, Point)
    hsz = size//2
    g = None

    def shift(p, x, y):
        return p[0]+x, p[1]+y

    if dir is 'up':
        g = lambda p: (shift(p, 0, -hsz), shift(p, 0, hsz))
    elif dir is 'down':
        g = lambda p: (shift(p, 0, hsz), shift(p, 0, -hsz))
    elif dir is 'left':
        g = lambda p: (shift(p, -hsz, 0), shift(p, hsz, 0))
    elif dir is 'right':
        g = lambda p: (shift(p, hsz, 0), shift(p, -hsz, 0))

    return g


def calc_angle(origin, target):
    x = target.x - origin.x
    y = target.y - origin.y

    cosine = x / ((x * x + y * y) ** 0.5)

    from math import acos, pi
    return acos(cosine) / 2 / pi * 360


def round_each(input):
    return tuple(map(lambda a: int(round(a)), input))


class Hierarchy:
    def __init__(self, hrki):
        self.hierarchy = hrki

    def tour(self, node, layer=0, visual=False):
        def p(text, n=''):
            print '%s%s%s' % ('\t' * layer, text, n)

        p = p if visual else lambda *x: None

        while True:
            p('> ', node)
            if self.hierarchy[node][1] != -2:
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

        if idx == 0:
            self.hierarchy[0][1] = -2
            return

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


class ParkingLot:
    def __init__(self, contour):
        self.contour = contour
        self.rect = cv2.boundingRect(contour)
        self.corners = calc_rect_points(self.rect)

        points = np.array(self.corners)
        self.center = cv2.minEnclosingCircle(points)[0]
        self.center = tuple(map(int, self.center))

        self.entranceL = self.corners[3]
        self.entranceR = self.corners[2]

        self.direction = None

    def set_dircetion(self, dir):
        self.direction = dir

    def draw(self, img):
        print 'drawing'
        c = icolor.next()

        # rectct = np.array([[pt] for pt in self.corners], dtype=np.int32)
        # img = cv2.drawContours(img, [rectct], 0, c)
        p1, _, p2, _ = self.corners
        cv2.rectangle(img, p1, p2, c, 1)

        print self.center
        cv2.circle(img, tuple(map(int, self.center)), 10, c)

        print self.entranceL, self.entranceR
        cv2.line(img, self.entranceL, self.entranceR, c, 3)

        p1, p2 = direction_arrow_gen(self.direction, 50)(self.center)
        print p1, p2
        cv2.arrowedLine(img, p2, p1, c, 2)

        return img


colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255)
]

icolor = itertools.cycle(colors)
