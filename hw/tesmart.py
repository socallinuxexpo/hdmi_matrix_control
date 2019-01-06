'''
TESmart.py:

Module containing TESmart matix driver code, for interacting with the TESmart matrix driver.

@author mproctor13
'''
import serial
import time
import threading
import logging
import random
import hw.matrix


class TESmartMatrix(hw.matrix.MatrixDriver):
  '''
  TESmartMatrix driver used to drive the TESmart matrix.
  '''
  def __init__(self, port, name="TESmartMatrix"):
    '''
    Open up the serial port owning this driver
    @param port: port string to open up
    @param name: name of the thread
    '''
    super().__init__(inputs=4, outputs=4, name=name)
    self.port = serial.Serial(port)

  def setup():
    '''
    Initial setup for this matrix. Send out the initial write.
    '''
    self.serial_port.write(b'MT00RD0000NT')
    
  def loop(self):
    '''
    Runs one iteration of the loop to process this driver
    '''
    data = self.serial_port.read(48)
    if len(data) == 48:
        self.channels = str(data)
    else:
        logging.warning("Unexpected message: %s", data)
    super().loop()

  def assign(out_chan, in_chan):
    '''
    Assign a given input channel to a given output channel
    @param out_chan: output channel
    @param in_chan: input channel
    '''
    logging.debug("Assigning %d to %s", (out_chan, in_chan))
    assert out_chan < self.outputs, "Invalid output channel %d" % out_chan
    assert in_chan < self.inputs, "Invalid input channel %d" % in_chan
    self.port.write(b"MT00SW%02d%02dNT" % (out_chan, in_chan))

  def getOutput(self, port):
    # LINK:O1I2;O2I2;O3I2;O4I1;O5I2;O6I1;O7I9;O8I2;END
    start = 5+(5*(port-1))
    logging.debug( "port=[%s] part=[%s]" % (port, str(self.status)[start+5]) ) 
    return int(self.status[start+5])

  @staticmethod
  def outputString(outport, inport):

  def setOutput(self, outport, inport):
    logging.debug( "setOutput got set outport %s to inport %s" % (outport, inport) )
    self.serial_port.write(TESmartMatrix.outputString(outport,inport))
    time.sleep(0.1)
    self.serial_port.write(b'MT00RD0000NT')
    time.sleep(0.1)
    
  def countUp(self):
    self.serial_port.write(b'MT00SW0000NT')
    time.sleep(0.1)
    self.serial_port.write(b'MT00RD0000NT')
    time.sleep(0.1)

