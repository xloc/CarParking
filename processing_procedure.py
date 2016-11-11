import cv2
import numpy as np
import utilfun as uf
import criteria


def threshold_process(img, blur_size=7, threshold=100):
    # type: (np.ndarray, int, int) -> np.ndarray
    """
    Method for smoothly thresholding image
    :param img: Input image in grey scale
    :param blur_size: Gaussian kernel size
    :param threshold: Threshold value
    :return: thresholded image
    """
    img_threshold = np.copy(img)

    gaussian_kernel = (blur_size, blur_size)
    img_threshold = cv2.GaussianBlur(img_threshold, gaussian_kernel, 0)
    _, img_threshold = cv2.threshold(
        img_threshold, threshold, 100, type=cv2.THRESH_BINARY_INV)

    return img_threshold


def find_contour(img):
    # type: (np.ndarray) -> object
    """
    Find Contour Process
    :param img: thresholded image
    :return: contours and hierarchy
    """
    imcotr = np.copy(img)
    image, contours, hierarchy = cv2.findContours(
        imcotr,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_NONE
    )

    return contours, hierarchy[0]


def filtering_size_overlap(contours, hierarchy,
                           min_area=criteria.MIN_AREA_CRITERIA,
                           min_area_diff=criteria.MIN_AREA_DIFF_CRITERIA,
                           min_dist=criteria.MIN_DISTANCE_CRITERIA):
    # type: (list, Hierarchy, int, int, int) -> uf.Hierarchy

    # Iteration init
    """
    Small and overlapped contour elimination
    :param contours: Contour input
    :param hierarchy: Hierarchy structure
    :param min_area: Minimum contour size
    :param min_area_diff: Minimum area difference
    :param min_dist: Minimum distance between center points of contours
    :return:
    """
    last_area = 0
    last_o = (0, 0)

    for ctidx, l in hierarchy.tour(0):
        ct = contours[ctidx]

        area = cv2.contourArea(ct)

        if area < min_area:
            hierarchy.delete_node(ctidx)
            continue

        o, r = cv2.minEnclosingCircle(ct)

        if abs(area - last_area) < min_area_diff:
            if uf.dist(o, last_o) < min_dist:
                hierarchy.delete_node(ctidx)
                continue

        last_area = area
        last_o = o

    return hierarchy


def filtering_hollow(hierarchy,
                     min_count=criteria.MIN_SUBCONTOUR_COUNT):
    # type: (Hierarchy, int) -> Hierarchy
    """
    Using Min nested contours number Determine validation
    :param hierarchy: Hierarchy need inspect
    :param min_count: Minimum contours count that the top layerhierarchy should contain
    :return: inspected hirerarchy
    """
    stat = {}
    grandpaidx = 0
    for i, l in hierarchy.tour(0):
        if l == 0:
            grandpaidx = i
            stat[i] = 0
        else:
            stat[grandpaidx] += 1

    satisfied_contour = []
    for k, v in stat.items():
        if v >= min_count:
            satisfied_contour.append(k)

    return satisfied_contour


def perspective_param(quadrangle, plane_size):
    # type: (np.ndarray, tuple) -> np.ndarray
    width, height = plane_size

    field = np.array([
            (0, 0),
            (width, 0),
            (width, height),
            (0, height)
        ], dtype=np.float32)
    quadrangle = quadrangle[:, 0, :].astype(np.float32)

    # Correct orbital direction
    rotfield = np.cross(field[1]-field[0], field[2]-field[1])
    rotbound = np.cross(quadrangle[1] - quadrangle[0], quadrangle[2] - quadrangle[1])
    if rotfield*rotbound < 0:
        quadrangle = quadrangle[::-1]

    # Origin align
    dist2origin = []
    for idx, pt in enumerate(quadrangle):
        dist2origin.append((idx, uf.dist(pt, (0, 0))))
    dist2origin.sort(key=lambda item: item[1])
    upperleftidx = dist2origin[0][0]

    fixed_bound = [quadrangle [(i + upperleftidx) % 4]
                   for i in range(4)]
    fixed_bound = np.array(fixed_bound)

    quadrangle = fixed_bound

    param = cv2.getPerspectiveTransform(quadrangle, field)
    return param


def warp_perspective(image, param, plane_size):
    width, height = plane_size

    img = cv2.warpPerspective(image, param, (width, height))
    return img


