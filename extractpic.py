import numpy
import struct


def stream2image(stream, size):
    # type: (io.BytesIO, tuple) -> numpy.array

    stream.seek(0)
    pixels = size[0]*size[1]*3
    listed = struct.unpack('={}B'.format(pixels), stream.read())

    shape = (size[1], size[0], 3)
    mtx = numpy.array(listed, dtype=numpy.uint8).reshape(shape)

    return mtx
