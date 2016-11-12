import cv2
import itertools
import numpy as np
import criteria
import utilfun as uf
from utilfun import imshow
import processing_procedure as prop


def perspective_analyse(img, threshold=100):

    # Section: Threshold processing

    imthres = prop.threshold_process(img, blur_size=7, threshold=threshold)

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

    # # Debug Image Drawing
    # imdebug = cv2.cvtColor(imthres, code=cv2.COLOR_GRAY2BGR)
    # for ctidx, l in nest.tour(0):
    #     uf.drawContour(imdebug, contours[ctidx])
    # imshow(imdebug)

    assert len(valid_contour_roots) == 1, \
        'Valid contour root count is not 1 (%d found)'%len(valid_contour_roots)

    rootidx = valid_contour_roots[0]


    # Section: Perspective transform

    bound = uf.polygonFit(contours[rootidx])

    # Debug Image Drawing
    imdebug = cv2.cvtColor(imthres, code=cv2.COLOR_GRAY2BGR)
    uf.drawContour(imdebug,bound)
    imshow(imdebug)

    pspt_param = prop.perspective_param(bound, (1000, 300))

    return pspt_param


# # Debug Image Drawing
# for ctidx,l in nest.spot(0):
#     cv2.drawContours(imdebug, [contours[ctidx]], 0, uf.icolor.next())
# imshow(imdebug)

def playground_analyse(imtailored):
    """

    :param imtailored: p-transformed non-threshold image
    :return: Playground object, Threshold Image
    """
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

    # # Debug Image Drawing
    # imdebug = cv2.cvtColor(imtailored, code=cv2.COLOR_GRAY2BGR)
    # for ctidx,l in nest.spot(0):
    #     cv2.drawContours(imdebug, [contours[ctidx]], 0, uf.icolor.next())
    # imshow(imdebug)

    # Find inner bound index
    inner_bound_idx = sorted([(i, cv2.contourArea(contours[i]))
                              for i, _ in nest.spot(0)],
                             key=lambda a: a[1])[-1][0]
    nest.delete_node(inner_bound_idx)
    inner_bound = contours[inner_bound_idx]

    # # Debug Image Drawing
    # uf.drawContour(imdebug,contours[inner_bound_idx])
    # imshow(imdebug)

    def each_contour():
        for i, l in nest.spot(0):
            yield contours[i]

    return PlayGround(each_contour), imtailored


class PlayGround:
    def __init__(self, contours):
        places = []
        self.places = places

        for ct in contours():
            lot = uf.ParkingLot(ct)
            places.append(lot)

        assert len(places) == 5, 'Not only 5 contour found'

        places.sort(key=lambda a: a.center[0])
        directions = ['down', 'right', 'left', 'down', 'up']
        for p, d in zip(places, directions):
            p.set_dircetion(d)

    def draw(self, image):
        for p in self.places:
            p.draw(image)


if __name__ == '__main__':
    # Load Image
    img = cv2.imread('playground.jpg')
    # Convert Color
    img = cv2.cvtColor(img, code=cv2.COLOR_BGR2GRAY)
    # Resize
    img = uf.resize2(img, 1000)
    # Analyse perspective parameter
    pspt_param = perspective_analyse(img)
    # Do inverse perspective transformation
    imtailored = prop.warp_perspective(img, pspt_param, (1000, 300))
    # Playground analyse
    playground, imthres = playground_analyse(imtailored)

    imdebug = cv2.cvtColor(imthres, cv2.COLOR_GRAY2BGR)
    playground.draw(imdebug)
    imshow(imdebug)

