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
In this example code, the internal serial ports are first initalized in order to test the matrix. The sleep function is then used to delay the long enough for the set up of the arduino. This allows the arduino to prepare for serial communication. A call to the start function is uitlized to set up and run the internal read/write (io) thread.

The driver code has its own internal io thread as it allows the thread to have a singular ownership over the serial port. Any request to get or set the state of the matrix box has to go through the io thread. 

Assign and read are calls that are put into a queue in order for the code to take multiple inputs at once. Read is the function that gets the state of the numbers presented on the matrix box. This then allows the thread to cache the read call into memory.

## ScaleMatrix (Follows above TESMART MATRIX CONTROL)

The Scale Matrix is a variant (subclass) of the TESmart class above. It operates in the same way, however; on a set interval it will send "special" messages that are intended to be pulled out of the serial stream in-transit. In this way, the UART interface can be used to communicate to multiple devices (specifically the TESMatrix and a snooper used to display data on an OLED screen).

The messages are simple and follow the following format:
```<KEY :MSG                 >```

Where `<` starts the special message. This is followed by a 4 character key, then a `:`, then a 20 character message, and finally terminated by a `>`.

**Example:**
```<Host:example.com>```

The ScaleMatrix assembles these messages internally and the user need take no other action.  However, if an internal error should be reported the following method may be called:

```
scalmat.error("Some error message; will be truncated to 20 characters")
```

### Example Code Usage 
```python
driver = hdmi_matrix_controller.hw.scalemat.ScaletMatrix("/dev/ttyUSB0")
time.sleep(6) #6 seconds needed for arduino setup delay 
driver.start()
#...
driver.error("Report this error")
```


