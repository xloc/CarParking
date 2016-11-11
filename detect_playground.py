import cv2
import itertools
import numpy as np
import criteria
import utilfun as uf
from utilfun import imshow
import processing_procedure as prop


def perspective_analyse(img):

    height, width = img.shape

    factor = float(width) / 1000
    img = cv2.resize(img, dsize=(1000, int(height / factor)),
                     interpolation=cv2.INTER_LINEAR)

    # Section: Threshold processing

    imthres = prop.threshold_process(img, blur_size=7)

    # Section: Find contours

    contours, hierarchy = prop.find_contour(imthres)

    # Section: Contour filtering

    # Debug purpose, for colorful drawing
    imdebug = cv2.cvtColor(imthres, code=cv2.COLOR_GRAY2BGR)

    # Prepare hierarchy
    nest = uf.Hierarchy(hierarchy)


        # Subsection: Area and Distance filtering

    nest = prop.filtering_size_overlap(contours, nest, min_area=1000)

        # Subsection: Min nested contour count filtering

    valid_contour_roots = prop.filtering_hollow(nest, min_count=6)

    assert len(valid_contour_roots) == 1, 'More than 1 valid contour root found'

    rootidx = valid_contour_roots[0]


    # Section: Perspective transform

    bound = uf.polygonFit(contours[rootidx])

    # # Debug Image Drawing
    # imdebug = cv2.cvtColor(imthres, code=cv2.COLOR_GRAY2BGR)
    # uf.drawContour(imdebug,bound)
    # imshow(imdebug)

    pspt_param = prop.perspective_param(bound, (1000, 300))

    return pspt_param


# # Debug Image Drawing
# for ctidx,l in nest.spot(0):
#     cv2.drawContours(imdebug, [contours[ctidx]], 0, uf.icolor.next())
# imshow(imdebug)

def playground_analyse(imtailored):
    # Section: Threshold processing

    imtailored = prop.threshold_process(imtailored, blur_size=7)

    # Section: 2nd Contours find
    contours, hierarchy = prop.find_contour(imtailored)

    # Section: 2nd Contours filtering
    # Prepare hierarchy
    nest = uf.Hierarchy(hierarchy)

        # Subsection: 2nd Area and Distance filtering

    nest = prop.filtering_size_overlap(contours, nest, min_area=1000)

        # Subsection: May need hierarchy criteria


    imdebug = cv2.cvtColor(imtailored, code=cv2.COLOR_GRAY2BGR)

    # Debug Image Drawing
    for ctidx,l in nest.spot(0,visual=True):
        cv2.drawContours(imtd, [contours[ctidx]], 0, uf.icolor.next())
    imshow(imdebug)

    # Calculate center line
    centerline = uf.calcline((0, 150), (1000, 150))

    # Find inner bound index
    inner_bound_idx = sorted([(i, cv2.contourArea(contours[i]))
                              for i, _ in nest.spot(0)],
                             key=lambda a: a[1])[-1][0]
    nest.delete_node(inner_bound_idx)
    inner_bound = contours[inner_bound_idx]

    # # Debug Image Drawing
    # uf.drawContour(imdebug,contours[inner_bound_idx])
    # imshow(imdebug)


    places = []
    for i, l in nest.spot(0):
        ct = contours[i]
        pklt = uf.ParkingLot(ct)
        places.append(pklt)
        pklt.determin_entrance(centerline)


    assert len(places) == 5, 'Not only 5 contour found'





    # # Debug Image Drawing
    # for pl in places:
    #     pl.draw(imdebug)
    # imshow(imdebug)

if __name__ == '__main__':
    # Load Image
    img = cv2.imread('playground.jpg')
    img = cv2.cvtColor(img, code=cv2.COLOR_BGR2GRAY)
    # Analyse perspective parameter
    pspt_param = perspective_analyse(img)
    # Do inverse perspective transformation
    imtailored = prop.warp_perspective(img, pspt_param, (1000, 300))
    imshow(imtailored)
    # Playground analyse
    playground_analyse(imtailored)

