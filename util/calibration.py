import numpy as np
import cv2

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


def calibrate(board_size, file_iter):
    # Notice : Use number of corners, but the order doesn't matter
    boardCol, boardRow = board_size

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    # objp = np.zeros((6*7,3), np.float32)
    # objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

    global objpoints, imgpoints, t_objpoints

    t_objpoints = np.zeros((boardRow * boardCol, 3), np.float32)
    t_objpoints[:, :2] = np.mgrid[0:boardCol, 0:boardRow].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    for imgFile in file_iter:
        add_points_from_file(imgFile, board_size)

    cv2.destroyAllWindows()

    gray = cv2.imread(imgFile, cv2.IMREAD_GRAYSCALE)

    # Calibrating
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    show_undistorted_img(imgFile, mtx, dist)


def add_points_from_file(path, board_size):
    global objpoints, imgpoints, t_objpoints

    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, board_size, None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(t_objpoints)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        if __debug__:
            imgr = cv2.drawChessboardCorners(img, board_size, corners, ret)
            img = cv2.drawChessboardCorners(img, board_size, corners2, ret)

            cv2.imshow('img', img)
            cv2.imshow('raw corners', imgr)
            cv2.waitKey(0)
            cv2.destroyWindow('img')
            cv2.destroyWindow('raw corners')


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

if __name__ == '__main__':

    calibrate((9, 6), ['left01.jpg'])