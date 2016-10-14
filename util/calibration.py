import numpy as np
import cv2
import glob

# Notice : Use number of corners, but the order doesn't matter
boardRow = 9
boardCol = 6

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
# objp = np.zeros((6*7,3), np.float32)
# objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

objp = np.zeros((boardRow*boardCol,3), np.float32)
objp[:,:2] = np.mgrid[0:boardCol,0:boardRow].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.


def add_points_from_file(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (boardCol, boardRow), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        if __debug__:
            imgr = cv2.drawChessboardCorners(img, (boardCol, boardRow), corners, ret)
            img = cv2.drawChessboardCorners(img, (boardCol, boardRow), corners2, ret)

            cv2.imshow('img', img)
            cv2.imshow('raw corners', imgr)
            cv2.waitKey(0)
            cv2.destroyWindow('img')
            cv2.destroyWindow('raw corners')

for imgFile in ['left01.jpg']:
    add_points_from_file(imgFile)

cv2.destroyAllWindows()

img = cv2.imread(imgFile)

# Calibrating
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img.shape[0:2][::-1],None,None)

def show_undistorted_img(path, mtx, dist):
    # Prepare image
    img = cv2.imread(path)
    h, w = img.shape[:2]
    camera_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    print camera_mtx, roi
    # undistort
    dst = cv2.undistort(img, mtx, dist, None, camera_mtx)
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    cv2.imwrite('calibresult.png', dst)
    cv2.imshow('result', dst)
    cv2.waitKey(0)


show_undistorted_img(imgFile, mtx, dist)