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

colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255)
]

edge = cv2.cvtColor(edge, code=cv2.COLOR_GRAY2BGR)

dist2 = lambda p, q: (p[0]-q[0])**2 + (p[1]-q[1])**2

fcontours = []

MIN_AREA_CRITERIA = 10
MIN_DISTANCE_CRITERIA = 10

last_area = 0
last_o = (0, 0)
for ct in contours:
    area = cv2.contourArea(ct)

    if area < 100:
        continue

    o, r = cv2.minEnclosingCircle(ct)

    if abs(area - last_area) < MIN_AREA_CRITERIA:
        if dist2(o, last_o) < MIN_DISTANCE_CRITERIA:
            continue

    last_area = area
    last_o = o

    fcontours.append(ct)

contours = fcontours

# print [contour.shape for contour in contours][0:5]


# print contours[0]


# for ct in contours:
#     rorect = cv2.minAreaRect(ct)
#     rectpts = cv2.boxPoints(rorect)
#     rectct = np.array([[pt] for pt in rectpts], dtype=np.int32)
#     print rectct
#
#     img = edge
#     img = cv2.drawContours(img, [rectct], 0, (255, 255, 0))
#     imshow(img)




import itertools
icolor = itertools.cycle(colors)

drawn = edge

for i in range(len(contours)):
    cparam = cv2.minEnclosingCircle(contours[i])
    print cparam

    center, radius = cparam

    drawn = cv2.drawContours(edge, contours, i, color=icolor.next());
    drawn = cv2.circle(
        drawn,
        center=tuple(map(int, center)),
        radius=int(radius),
        color=icolor.next())

    imshow(drawn)
