# pylint: disable=missing-docstring
import logging
import threading
import time

import hdmi_matrix_controller.hw.scalemat


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(logging.StreamHandler())

SLEEP_WAIT = 7

LOGGER.debug("Initializing driver")
DRIVER = hdmi_matrix_controller.hw.scalemat.ScaleMatrix("/dev/ttyUSB0")

LOGGER.debug("Waiting %s", SLEEP_WAIT)
time.sleep(SLEEP_WAIT)

LOGGER.debug("Setting up driver")
DRIVER.start()


def runner():
    # for i in [0, 1, 2, 3]:
    #    driver.assign(i, 0)

    for i in [0, 1, 2, 3]:
        for j in [0, 1, 2, 3]:
            LOGGER.debug("Setting %s,%s", i + 1, j + 1)
            DRIVER.assign(i, j)
            time.sleep(1)
            port_status = DRIVER.read(i)
            # print(j + " = " +port_status)
            assert j == port_status
            # assert read == j, "Read wrongo %d vs %d" % (read, j)
            time.sleep(1)


class Tmp(threading.Thread):
    def run(self):
        runner()
        DRIVER.running = False


TWO = Tmp()
TWO.start()
