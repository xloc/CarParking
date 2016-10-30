from struct import unpack
import numpy as np
import cv2

with open('bgr_raw', 'rb') as f:
    data = f.read()

print len(data)


imageSize = (320, 240)
byteCount = imageSize[0]*imageSize[1]*3

listed = unpack('=%dB' % byteCount, data)

print len(listed)


img = np.array(listed, dtype=np.uint8)

img = img.reshape((240, 320, 3))

print img.shape


cv2.imshow('test', img)
cv2.waitKey(0)
