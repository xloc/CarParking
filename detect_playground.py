import cv2
import itertools
import numpy as np
import util


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


# Prepare hierarchy
hierarchy = hierarchy[0]
m_hiera = util.Hierarchy(hierarchy)


EXPECTED_SUBCONTOUR_COUNT = 6


def hierarchy_criteria():
    stat = {}
    grandpaidx = 0
    for i, l in m_hiera.tour(0):

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

valid_contour_roots = hierarchy_criteria()

assert len(valid_contour_roots) == 1, 'More than 1 valid contour root found'

rootidx = valid_contour_roots[0]






# Delete criteria specification
MIN_AREA_CRITERIA = 100
MIN_AREA_DIFF_CRITERIA = 10
MIN_DISTANCE_CRITERIA = 10

# Iteration init
last_area = 0
last_o = (0, 0)

for ctidx, l in m_hiera.spot(rootidx):
    ct = contours[ctidx]

    area = cv2.contourArea(ct)

    if area < MIN_AREA_CRITERIA:
        m_hiera.delete_node(ctidx)
        continue

    o, r = cv2.minEnclosingCircle(ct)

    if abs(area - last_area) < MIN_AREA_DIFF_CRITERIA:
        if util.dist2(o, last_o) < MIN_DISTANCE_CRITERIA:
            m_hiera.delete_node(ctidx)
            continue

    last_area = area
    last_o = o




drawn = np.copy(edge)


for i, l in m_hiera.spot(rootidx):
    # print i
    drawn = cv2.drawContours(drawn, [contours[i]], 0, color=util.icolor.next());

# imshow(drawn)




class ParkingLot:
    def __init__(self, contour):
        self.contour = contour
        self.rect = cv2.minAreaRect(contour)
        self.corners = cv2.boxPoints(self.rect)

    def determin_entrance(self, centerline):
        corners = self.corners

        dist_corner_map = []
        for p in corners:
            dist_corner_map.append(
                (util.dist2line(p, centerline), p)
            )

        dist_corner_map.sort(key=lambda mp:mp[0])

        print dist_corner_map

    def draw(self, img):
        print 'drawing'
        rectct = np.array([[pt] for pt in self.corners], dtype=np.int32)
        return cv2.drawContours(img, [rectct], 0, (255, 255, 0))


pp = np.copy(edge)

places = []

for i, l in m_hiera.spot(rootidx):
    ct = contours[i]

    if cv2.contourArea(ct) < 10000:
        pl = ParkingLot(ct)

        # pp = pl.draw(pp)

        places.append(pl)

# imshow(pp)

bound = contours[rootidx]

eps = 0.05 * len(bound)
bound = cv2.approxPolyDP(bound, eps, closed=True)
# print len(bound)

pp = cv2.drawContours(pp, [bound], 0, (255, 255, 0))

imshow(pp)