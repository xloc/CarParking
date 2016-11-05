import io
import time
import threading
import picamera

# import pydevd
# pydevd.settrace('192.168.1.111', port=52481,           =True)

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

starttime = 0
endtime = 0
capcount = 0
def streams_provider():
    global imgdata
    stream = io.BytesIO()
    prevtime = time.clock()

    global starttime, endtime, capcount
    starttime = time.clock()
    while not done:
        capcount += 1

        yield stream

        stream.seek(0)
        with lock:
            imgdata = stream.read()
        frameCaptured.set()

        stream.seek(0)
        stream.truncate()

    endtime = time.clock()

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

    time.sleep(1)

    print 'time elapse', endtime-starttime
    print 'capture count', capcount
    print 'frequence', capcount/(endtime-starttime)
