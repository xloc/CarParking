import cv2
import utilfun as uf
import processing_procedure
import detect_playground
import processing_procedure as prop
import math

from utilfun import imshow


def car_analysis(image):
    """

    :param image: Image which is thresholded and after perspective transoformed
    :return:
    """
    # # Debug Image Drawing
    # imshow(imthres)

    # Find and generally Filter contours
    contours, hierarchy = prop.find_contour(image)
    nest = uf.Hierarchy(hierarchy)
    # Circles area :large=1600, small=340
    prop.filtering_size_overlap(contours, nest, min_area=200, max_area=2000)

    # # Debug Image Draw and output
    # imdebug = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # print 'One iteration'
    # for i, l in nest.tour(0):
    #     ct = contours[i]
    #     uf.drawContour(imdebug, ct)
    #     print '%5.2f' % cv2.contourArea(ct)
    #     imshow(imdebug)

    # Do specific circle Filter
    marks = []
    for ctidx, l in nest.tour(0):
        ct = contours[ctidx]
        area = cv2.contourArea(ct)
        (x, y), r = cv2.minEnclosingCircle(ct)
        rdarea = 3.14 * r ** 2

        # print '%5.2f' % ((rdarea-area)/rdarea)

        if (rdarea-area)/rdarea > 0.2:
            nest.delete_node(ctidx)
        else:
            marks.append(((x, y), area))

    # # Debug Iterate hierarchy
    # imdebug = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # print 'After shape filtering'
    # for i, l in nest.tour(0):
    #     ct = contours[i]
    #
    #     uf.drawContour(imdebug, ct)
    #
    #     area = cv2.contourArea(ct)
    #     (x, y), r = cv2.minEnclosingCircle(ct)
    #     rdarea = 3.14 * r ** 2
    #
    #     print 'area:%15.2f\tratio:%15.2f' % (area, (rdarea - area) / rdarea)
    #     imshow(imdebug)

    # # Debug Iterate marks
    # imdebug = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # print 'After shape filtering, circle array'
    # for p, area in marks:
    #     p = uf.round_each(p)
    #     cv2.circle(imdebug, p, int(area**0.5), uf.icolor.next())
    #     print 'radius', int(area**0.5)
    #     imshow(imdebug)

    # Assert found only 2 circles
    assert len(marks) == 2, 'Found circle count is not 2'

    # Distinguish two different circle
    marks.sort(key=lambda a: a[1])

    # Debug Print sorting results
    # print 'Sorted'
    # for p, area in marks:
    #     print 'radius', int(area**0.5)

    # Extract properties of circles
    smallo = uf.Point._make(marks[0][0])
    largeo = uf.Point._make(marks[1][0])

    # # Debug Output
    # print smallo
    # print largeo

    angle = uf.calc_angle(smallo, largeo)
    # # Debug Output
    # print angle

    # # Debug Output
    # imdebug = cv2.cvtColor(imthres, cv2.COLOR_GRAY2BGR)
    # for ct, l in nest.tour(0):
    #     uf.drawContour(imdebug, contours[ct])
    # imshow(imdebug)

    return smallo, angle


def draw_car(image, o, a, color):

    o = uf.round_each(o)
    cv2.circle(image, o, 5, color, thickness=5)

    ptar = (o[0] + 60 * math.cos(math.radians(-a)),
            o[1] + 60 * math.sin(math.radians(-a)))
    ptar = uf.round_each(ptar)
    cv2.arrowedLine(image, o, ptar, color, thickness=2)

    return image


if __name__ == '__main__':
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
    # Threshold image
    imthres = prop.threshold_process(imtailored)

    # Analyse image for center and angle
    center, angle = car_analysis(imthres)

    imdebug = cv2.cvtColor(imthres, cv2.COLOR_GRAY2BGR)
    imdebug = draw_car(imdebug, center, angle, (0, 255, 0))
    imshow(imdebug)
