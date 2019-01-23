This document is used to decribe the included software packages as well as the usage of the HDMI matrix controller. 

## TESMART MATRIX CONTROL 

The TESMART driver code is a threaded script that communicates with the TESMART matrix box. It is used to be intergrated with
the SCALE/AV software systems through python. 

### Example Code Usage 
```python
driver = hdmi_matrix_controller.hw.tesmart.TESmartMatrix("/dev/ttyUSB0")
time.sleep(6) #6 seconds needed for arduino setup delay 
driver.start()
```
In this example code, the internal serial ports are first initalized in order to test the matrix. The sleep function is then used to delay the set up of the arduino. This allows the arduino to prepare for serial communication. A call to the start function is uitlized to set up the internal read/write (io) thread.

The driver code has its own internal io thread as it allows the thread to have a singular ownership over the serial port. Any request to get or set the state of the matrix box has to go through the io thread. 

Assign and read are calls that are put into a queue in order for the code to take multiple inputs at once. Read is the function that gets the state of the numbers presented on the matrix box. This then allows the thread to cache the read call into memory.

