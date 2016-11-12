import serial

s = serial.Serial('/dev/tty.MS2016-DevB', baudrate=38400)

s_velo = 0
s_angle = 0


def control(velocity, angle):
    s.write("# %6.3f %7.3f\r\n" % (velocity, angle))


def set_angle(a):
    control(s_velo, a)


def set_velo(v):
    control(v, s_velo)
