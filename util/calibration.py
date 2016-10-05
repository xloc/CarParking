import numpy as np
import cv2
import glob

sizex, sizey = 6, 8

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(sizex,5,0)
objp = np.zeros((sizex*sizey,3), np.float32)
objp[:,:2] = np.mgrid[0:sizey,0:sizex].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = ["./cali.jpg"]

img = cv2.imread("./cali.jpg", cv2.CV_LOAD_IMAGE_GRAYSCALE)
cv2.namedWindow("debug")
cv2.imshow("debug",img)
cv2.waitKey(0)

cv2.namedWindow("debug")
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (sizey,sizex),None)


    # If found, add object points, image points (after refining them)
    if ret == True:
        print "here"
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (sizey,sizex), corners2,ret)
        cv2.imshow('img',img)
        cv2.waitKey(0)

cv2.destroyAllWindows()