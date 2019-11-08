""" Driver constant"""
import serial
from . import hw
try:
    DRIVER = hw.TESmartMatrix("/dev/ttyUSB0")
except Exception as exc:
    print("!!!!!!!!!!!!!!!!!!!!!!!!!! Exception: ", exc)
    DRIVER = hw.MatrixDriver()