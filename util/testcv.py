import cv2

im = cv2.imread("./cali.jpg", cv2.CV_LOAD_IMAGE_GRAYSCALE)

cv2.namedWindow("show")
cv2.imshow("show", im)
cv2.waitKey(0)

