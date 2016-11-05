import io
import time
import threading
import picamera
import copy

frameCaptured = threading.Event()

streamLock = threading.Lock()
picStream = io.BytesIO()

done = False


def get_framestream():
    if frameCaptured.wait():
        with streamLock:
            picStream.seek(0)
            stream = copy.copy(picStream)

        frameCaptured.clear()
        return stream


def streams_provider():
    while not done:
        with streamLock:
            picStream.seek(0)
            picStream.truncate()
            yield picStream
            frameCaptured.set()


def capture_loop():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 30
        camera.start_preview()
        time.sleep(2)
        camera.capture_sequence(streams_provider(), use_video_port=True)
