""" Driver constant"""
import serial
from . import hw
try:
    serial_port = serial.Serial("/dev/ttyUSB0")  # open serial port
    DRIVER = hw.TESmartMatrix(serial_port)
except:
    DRIVER = hw.MatrixDriver()