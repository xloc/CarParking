import io
import time
import threading
import picamera

# import pydevd
# pydevd.settrace('192.168.1.111', port=52481, stdoutToServer=True, stderrToServer=True)

frameCaptured = threading.Event()

lock = threading.Lock()
imgdata = 0

done = False


def get_framestream():
    # type: () -> string
    if frameCaptured.wait():
        with lock:
            data = imgdata

        frameCaptured.clear()
        return data


def streams_provider():
    global imgdata
    stream = io.BytesIO()

    while not done:
        yield stream

        stream.seek(0)
        with lock:
            imgdata = stream.read()
        frameCaptured.set()

        stream.seek(0)
        stream.truncate()


def capture_loop():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 30
        camera.start_preview()
        time.sleep(2)
        print 'start capture'
        camera.capture_sequence(streams_provider(),
                                use_video_port=True,
                                format='bgr')

if __name__ == '__main__':
    import cv2
    import extractpic

    threading.Thread(target=capture_loop).start()

    order = 0

    testing = True
    while testing:
        try:
            print "start %d" % order
            order += 1
            imgstr = get_framestream()
            img = extractpic.string2image(imgstr,
                                          (640, 480))
            cv2.imwrite('a%d.jpg' % order, img)
            time.sleep(1)
        except:
            break

    testing = False
    done = True
