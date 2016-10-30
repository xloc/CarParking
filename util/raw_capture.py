import time
import picamera
import io

with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.framerate = 24
    time.sleep(2)

    imgstream = io.BytesIO()
    camera.capture(imgstream, 'bgr')
    imgstream.seek(0)

    f = open('bgr_raw', 'w')
    f.write(imgstream.read())
    f.close()