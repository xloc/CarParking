import cv2
import utilfun as uf
import processing_procedure
import detect_playground
import processing_procedure as prop

from utilfun import imshow

# Load Image
img = cv2.imread('cell.jpg')
# Convert Color
img = cv2.cvtColor(img, code=cv2.COLOR_BGR2GRAY)
# Resize
img = uf.resize2(img, 1000)
# Analyse perspective parameter
pspt_param = detect_playground.perspective_analyse(img)
# Do inverse perspective transformation
imtailored = prop.warp_perspective(img, pspt_param, (1000, 300))


imthres = prop.threshold_process(imtailored)
imshow(imthres)

contours, hierarchy = prop.find_contour(imthres)
nest = uf.Hierarchy(hierarchy)
nest = prop.filtering_size_overlap(contours, nest, min_area=500, max_area=2000)


marks = []
for ctidx, l in nest.tour(0):
    ct = contours[ctidx]
    area = cv2.contourArea(ct)
    (x, y), r = cv2.minEnclosingCircle(ct)
    rdarea = 3.14 * r ** 2

    print (rdarea-area)/rdarea

    if (rdarea-area)/rdarea > 0.1:
        nest.delete_node(ctidx)
    else:
        marks.append(((x, y), area))

marks.sort(key=lambda a: a[1])

assert len(marks) == 2, 'Found circle count is not 2'

smallo = uf.Point._make(marks[0][0])
largeo = uf.Point._make(marks[1][0])

print smallo
print largeo


def calc_angle(po, pt):
    x = pt.x - po.x
    y = pt.y - po.y

    cosine = x / ((x*x+y*y)**0.5)

    from math import acos, pi
    return acos(cosine)/2/pi*360

print calc_angle(largeo, smallo)

imdebug = cv2.cvtColor(imthres, cv2.COLOR_GRAY2BGR)
for ct, l in nest.tour(0):
    uf.drawContour(imdebug, contours[ct])



imshow(imdebug)

# print circles
