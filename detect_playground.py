import cv2
import itertools
import numpy as np
import criteria
import utilfun as uf


def imshow(img):
    cv2.imshow('show', img)
    cv2.waitKey(0)


# Section: Load Image

img = cv2.imread('playground.jpg')
height, width, _ = img.shape

factor = float(width) / 1000
img = cv2.resize(img, dsize=(1000, int(height / factor)),
                 interpolation=cv2.INTER_LINEAR)


# Section: Find contours

imthres = np.copy(img)

imthres = cv2.cvtColor(imthres, code=cv2.COLOR_BGR2GRAY)
imthres = cv2.GaussianBlur(imthres, (7, 7), 0)
# imedge = cv2.Canny(imedge, 100, 15)
_, imthres = cv2.threshold(imthres, 100, 100, type=cv2.THRESH_BINARY_INV)

imcotr = np.copy(imthres)
image, contours, hierarchy = cv2.findContours(
    imcotr,
    cv2.RETR_TREE,
    cv2.CHAIN_APPROX_NONE
)


# Section: Contour filtering

# Debug purpose, for colorful drawing
im = cv2.cvtColor(imthres, code=cv2.COLOR_GRAY2BGR)

# Prepare hierarchy
hierarchy = hierarchy[0]
nest = uf.Hierarchy(hierarchy)


# Subsection: Area and Distance filtering

# Iteration init
last_area = 0
last_o = (0, 0)

for ctidx, l in nest.tour(0):
    ct = contours[ctidx]

    area = cv2.contourArea(ct)

    if area < criteria.MIN_AREA_CRITERIA:
        nest.delete_node(ctidx)
        continue

    o, r = cv2.minEnclosingCircle(ct)

    if abs(area - last_area) < criteria.MIN_AREA_DIFF_CRITERIA:
        if uf.dist(o, last_o) < criteria.MIN_DISTANCE_CRITERIA:
            nest.delete_node(ctidx)
            continue

    last_area = area
    last_o = o


# Subsection: Min nested contour count filtering

# Using Min nested contours number Determine validation
def hierarchy_criteria():
    stat = {}
    grandpaidx = 0
    for i, l in nest.tour(0):
        if l == 0:
            grandpaidx = i
            stat[i] = 0
        else:
            stat[grandpaidx] += 1

    satisfied_contour = []
    for k, v in stat.items():
        if v >= criteria.MIN_SUBCONTOUR_COUNT:
            satisfied_contour.append(k)

    return satisfied_contour

valid_contour_roots = hierarchy_criteria()

assert len(valid_contour_roots) == 1, 'More than 1 valid contour root found'

rootidx = valid_contour_roots[0]


# Section: Perspective transform

def polygonFit(contour, factor=0.05):
    # type: (object, float) -> np.ndarray
    eps = factor * len(contour)
    return cv2.approxPolyDP(contour, eps, closed=True)

def perspective_correct():
    bound = polygonFit(contours[rootidx])

    PG_WIDTH, PG_HEIGHT = (1000, 300)

    field = np.array([
            (0, 0),
            (PG_WIDTH, 0),
            (PG_WIDTH, PG_HEIGHT),
            (0, PG_HEIGHT)
        ], dtype=np.float32)
    bound = bound[:,0,:].astype(np.float32)

    # Correct orbital direction
    rotfield = np.cross(field[1]-field[0], field[2]-field[1])
    rotbound = np.cross(bound[1]-bound[0], bound[2]-bound[1])
    if rotfield*rotbound < 0:
        bound = bound[::-1]

    # Origin align
    dist2origin = []
    for idx, pt in enumerate(bound):
        dist2origin.append((idx, uf.dist(pt, (0, 0))))
    dist2origin.sort(key=lambda item: item[1])
    upperleftidx = dist2origin[0][0]

    fixed_bound = [
        bound[(i + upperleftidx) % 4]
                   for i in range(4)]
    fixed_bound = np.array(fixed_bound)

    print fixed_bound
    bound = fixed_bound

    mat = cv2.getPerspectiveTransform(bound, field)
    img = cv2.warpPerspective(imthres, mat, (PG_WIDTH, PG_HEIGHT))

    return img

imtailored = perspective_correct()





# Debug Image Drawing
for ctidx,l in nest.spot(0):
    cv2.drawContours(im, [contours[ctidx]], 0, uf.icolor.next())

# imshow(im)




# Section: 2nd Contours find

imcotr = np.copy(imtailored)
image, contours, hierarchy = cv2.findContours(
    imcotr,
    cv2.RETR_TREE,
    cv2.CHAIN_APPROX_NONE
)


# Section: 2nd Contours filtering

# Prepare hierarchy
hierarchy = hierarchy[0]
nest = uf.Hierarchy(hierarchy)


# Subsection: 2nd Area and Distance filtering

# Iteration init
last_area = 0
last_o = (0, 0)

for ctidx, l in nest.tour(0):
    ct = contours[ctidx]

    area = cv2.contourArea(ct)

    if area < criteria.MIN_AREA_CRITERIA:
        nest.delete_node(ctidx)
        continue

    o, r = cv2.minEnclosingCircle(ct)

    if abs(area - last_area) < criteria.MIN_AREA_DIFF_CRITERIA:
        if uf.dist(o, last_o) < criteria.MIN_DISTANCE_CRITERIA:
            nest.delete_node(ctidx)
            continue

    last_area = area
    last_o = o

# Section: May need hierarchy criteria



#

imtd = cv2.cvtColor(imtailored, code=cv2.COLOR_GRAY2BGR)

# # Debug Image Drawing
# for ctidx,l in nest.spot(0,visual=True):
#     cv2.drawContours(imtd, [contours[ctidx]], 0, uf.icolor.next())
#
# imshow(imtd)

rootidx = 0

places = []

for i, l in nest.spot(rootidx):
    ct = contours[i]

    pl = uf.ParkingLot(ct)

    imtd = pl.draw(imtd)

    places.append(pl)

    imshow(imtd)
