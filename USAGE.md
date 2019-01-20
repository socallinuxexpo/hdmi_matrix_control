This document is used to describe the usage of the HDMI matrix controller, and the software packages included with it. 

## TESMART MATRIX CONTROL 

The TESMART driver code communicates and is threaded with the TESMART matrix box. It is used to be intergrated with
the SCALE/AV software systems through python. 

### Example Code Usage 
```python
driver = hdmi_matrix_controller.hw.tesmart.TESmartMatrix("/dev/ttyUSB0")
time.sleep(6) #6 seconds needed for aurdino setup delay 
driver.start()
```
In this piece of code, it begins by initalzing the internal serial port in order to test the matrix. The sleep function is 
used to delay for the arudino set up which prepares for serial communication. The start function then sets up the internal 
read/write thread. 

The driver code has its own internal io thread. Ownership is important because it allows the thread to have a singular ownership
over the serial port. Any request to get the state of the matrix box or set the state has to go through the io thread. 

Assign and read are calls that are put into a queue where calls and runs are through one and another. A queue is needed in order
to take multiple inputs at once. Read is the function that gets the state of the numbers presented on the matrix box, where the
the thread cashes read to memory. 

