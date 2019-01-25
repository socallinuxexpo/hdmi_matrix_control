import time
import threading
import hdmi_matrix_controller.hw.scalemat
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

sleep_wait = 7

logger.debug("Initializing driver")
driver = hdmi_matrix_controller.hw.scalemat.ScaleMatrix("/dev/ttyUSB0")

logger.debug("Waiting %s", sleep_wait)
time.sleep(sleep_wait)

logger.debug("Setting up driver")
driver.start()

def runner():
    #for i in [0, 1, 2, 3]:
    #    driver.assign(i, 0)

    for i in [0, 1, 2, 3]:
        for j in [0, 1, 2, 3]:
            logger.debug("Setting %s,%s", i + 1, j + 1)
            driver.assign(i, j)
            time.sleep(1)
            port_status = driver.read(i)
            #print(j + " = " +port_status)
            assert j == port_status
            #assert read == j, "Read wrongo %d vs %d" % (read, j)
            time.sleep(1)

class Tmp(threading.Thread):
    def run(self):
        runner()
        driver.running = False

two = Tmp()
two.start()
