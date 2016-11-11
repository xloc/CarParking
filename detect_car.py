import cv2
import utilfun as uf
import processing_procedure
import detect_playground
import processing_procedure as prop

from utilfun import imshow

# Load Image
img = cv2.imread('mark.jpg')
# Convert Color
img = cv2.cvtColor(img, code=cv2.COLOR_BGR2GRAY)
# Resize
img = uf.resize2(img, 1000)
# Analyse perspective parameter
pspt_param = detect_playground.perspective_analyse(img)
# Do inverse perspective transformation
imtailored = prop.warp_perspective(img, pspt_param, (1000, 300))


imthres = processing_procedure.threshold_process(imtailored)
imshow(imthres)

circles = cv2.HoughCircles(imthres, cv2.HOUGH_GRADIENT, 1, 1, param1=200, param2=100);

print circles
