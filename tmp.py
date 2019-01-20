import time
import threading
import hdmi_matrix_controller.hw.tesmart

driver = hdmi_matrix_controller.hw.tesmart.TESmartMatrix("/dev/ttyUSB0")
driver.start()
time.sleep(0.5)
def runner():
    for i in [0, 1, 2, 3]:
        driver.assign(i, 0)
    time.sleep(5)

    for i in [0, 1, 2, 3]:
        for j in [0, 1, 2, 3]:
            driver.assign(i, j) 
            time.sleep(0.2)
            read = driver.read(i)
            print("Read: i=", read)
            #assert read == j, "Read wrongo %d vs %d" % (read, j)
            time.sleep(1)

class Tmp(threading.Thread):
    def run(self):
        runner()

two = Tmp()
two.start()
