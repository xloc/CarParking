import cv2
import numpy as np


def imshow(img):
    cv2.imshow('show', img)
    cv2.waitKey(0)

img = cv2.imread('playground.png')
img = cv2.resize(img, dsize=(0,0), fx=0.5, fy=0.5)


img = cv2.cvtColor(img, code=cv2.COLOR_BGR2GRAY)


edge = cv2.Canny(img, 100, 15)

# print edge.shape
edge = edge[300:588][:]
image, contours, hierarchy = cv2.findContours(
    edge,

    # cv2.RETR_TREE,
    cv2.RETR_LIST,

    cv2.CHAIN_APPROX_NONE)

colors = [
    (255,0,0),
    (0,255,0),
    (0,0,255),
    (255,255,0),
    (0,255,255),
    (255,0,255)
]

edge = cv2.cvtColor(edge, code=cv2.COLOR_GRAY2BGR)
print [contour.shape for contour in contours]


areas = []
for ct in contours:
    area = cv2.contourArea(ct)
    areas.append(area)

areas.sort()
print areas

import random
for i in range(len(contours)):
    drawn = cv2.drawContours(edge, contours, i, color=random.choice(colors));

imshow(drawn)



