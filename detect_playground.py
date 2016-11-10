import cv2
import itertools
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
                for subnode in self.tour(self.hierarchy[node][2], layer+1,visual):
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
        print 'del', idx

        shit = self.hierarchy[idx]
        shitnextidx = shit[0]
        shitprevidx = shit[1]

        if shitnextidx >= 0:
            self.hierarchy[shitnextidx][1] = shitprevidx
        if shitprevidx >= 0:
            self.hierarchy[shitprevidx][0] = shitnextidx

        bshit = self.hierarchy[shit[3]]
        if bshit[2] == idx:
            bshit[2] = shitnextidx

        # f = open('output', 'a')
        # f.write(str(self.hierarchy))
        # f.write('$')
        # f.close()
    # delete_node = lambda *args: None

    def copy(self):
        return Hierarchy(list(self.hierarchy))


m_hiera = Hierarchy(hierarchy)


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



# Utility function for distance eval
dist2 = lambda p, q: (p[0]-q[0])**2 + (p[1]-q[1])**2


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
        if dist2(o, last_o) < MIN_DISTANCE_CRITERIA:
            m_hiera.delete_node(ctidx)
            continue

    last_area = area
    last_o = o





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

icolor = itertools.cycle(colors)

drawn = edge


for i, l in m_hiera.spot(rootidx, visual=True):
# for i in [19, 21, 23, 25, 26, 28, 30, 31]:
#     print i
    drawn = cv2.drawContours(drawn, [contours[i]], 0, color=icolor.next());

    imshow(drawn)