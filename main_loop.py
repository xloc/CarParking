import cv2
import time
import numpy as np
import utilfun as uf
import processing_procedure as prop

import detect_car
import detect_playground

from utilfun import imshow

PLAYGROUND_PIC_SIZE = (1000, 300)
THRESHOLD_VALUE = 50
IMAGE_WIDTH = 1000

camera = cv2.VideoCapture(2)
assert camera.isOpened(), 'Camera is not properly opened'

# region PREPARE PICTURE FOR ANALYSIS
# Wait
time.sleep(1)
# Take a picture
valid, frame = camera.read()
# Grayed
gray = prop.grayed(frame)
# Resize
fitted = uf.resize2(gray, IMAGE_WIDTH)
# endregion
prepared = fitted


# region PERSPECTIVE ANALYSIS
pspt_param = detect_playground.perspective_analyse(prepared, threshold=THRESHOLD_VALUE)
# endregion
perspective_param = pspt_param


# region Inverse perspective transform
def warp_transform(image):
    return prop.warp_perspective(image, pspt_param, PLAYGROUND_PIC_SIZE)
# endregion
warp_transform = warp_transform



# region PLAYGROUND ANALYSIS

# Inverse transform
tailored = warp_transform(prepared)

# Analysis playground
playground, imthres = detect_playground.playground_analyse(tailored)
# endregion
playground = playground
imthres = imthres


imdebug = cv2.cvtColor(imthres, cv2.COLOR_GRAY2BGR)
playground.draw(imdebug)
imshow(imdebug)

exit()


# WORK LOOP
while True:
    # region PREPARE IMAGE FRAME
    valid, frame = camera.read()
    # endregion
    frame = frame

    # region PRE-PROCESSING
    # Grayed
    gray = prop.grayed(frame)
    # Resize
    fitted = uf.resize2(gray, IMAGE_WIDTH)
    # Warp transform
    tailored = warp_transform(fitted)
    # Threshold
    imthres = prop.threshold_process(tailored, threshold=THRESHOLD_VALUE)
    # endregion
    imout = imthres

    # region CAR GESTURE ANALYSE
    try:
        center, angle = detect_car.car_analysis(imout)



        imdebug = cv2.cvtColor(imout, cv2.COLOR_GRAY2BGR)
        imdebug = detect_car.draw_car(imdebug, center, angle, (0, 255, 0))
        imshow(imdebug)

    except AssertionError:
        print "DETECT CAR ERROR"
    # endregion
    # center, angle = center, angle

