import cv2
import numpy as np


def imshow(img):
    cv2.imshow('show', img)
    cv2.waitKey(0)


img = cv2.imread('playground.png')
img = cv2.resize(img, dsize=(0, 0), fx=0.5, fy=0.5)

img = cv2.cvtColor(img, code=cv2.COLOR_BGR2GRAY)

edge = cv2.Canny(img, 100, 15)

# print edge.shape
edge = edge[300:588][:]
image, contours, hierarchy = \
    cv2.findContours(
        edge,

        cv2.RETR_TREE,

        cv2.CHAIN_APPROX_NONE)


# For colorful drawing
edge = cv2.cvtColor(edge, code=cv2.COLOR_GRAY2BGR)

hierarchy = hierarchy[0]


def tour(node, layer=0, visual=False):
    def p(text):
        print '%s%s' % ('\t' * layer, text)

    p = p if visual else lambda x: None

    while True:
        p('> %s' % node)
        yield node, layer

        # tour child
        if hierarchy[node][2] >= 0:
            for subnode in tour(hierarchy[node][2], layer+1):
                yield subnode

        # if no next
        if hierarchy[node][0] >= 0:
            node = hierarchy[node][0]
        else:
            break

    p('<')


def spot(node):
    childidx = hierarchy[node][2]
    if childidx < 0:
        return

    for ni in tour(childidx):
        yield ni


EXPECTED_SUBCONTOUR_COUNT = 6


def hierarchy_criteria():
    stat = {}
    grandpaidx = 0
    for i, l in tour(0):

        if l == 0:
            grandpaidx = i
            stat[i] = 0
        else:
            stat[grandpaidx] += 1


    satisfied_contour = []
    for k, v in stat.items():
        if v > EXPECTED_SUBCONTOUR_COUNT:
            satisfied_contour.append(k)

    return satisfied_contour

print hierarchy_criteria()





'''
# Utility function for distance eval
dist2 = lambda p, q: (p[0]-q[0])**2 + (p[1]-q[1])**2

# Delete criteria specification
MIN_AREA_CRITERIA = 100
MIN_AREA_DIFF_CRITERIA = 10
MIN_DISTANCE_CRITERIA = 10

# Iteration init
fcontours = []
last_area = 0
last_o = (0, 0)

for ct in contours:
    area = cv2.contourArea(ct)

    if area < MIN_AREA_CRITERIA:
        continue

    o, r = cv2.minEnclosingCircle(ct)

    if abs(area - last_area) < MIN_AREA_DIFF_CRITERIA:
        if dist2(o, last_o) < MIN_DISTANCE_CRITERIA:
            continue

    last_area = area
    last_o = o

    fcontours.append(ct)

contours = fcontours




# for ct in contours:
#     rorect = cv2.minAreaRect(ct)
#     rectpts = cv2.boxPoints(rorect)
#     rectct = np.array([[pt] for pt in rectpts], dtype=np.int32)
#     print rectct
#
#     img = edge
#     img = cv2.drawContours(img, [rectct], 0, (255, 255, 0))

# imshow(img)

colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255)
]

import itertools
icolor = itertools.cycle(colors)

drawn = edge

for i in range(len(contours)):

    drawn = cv2.drawContours(edge, contours, i, color=icolor.next());

imshow(drawn)
'''