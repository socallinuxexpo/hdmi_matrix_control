import serial
import time
import threading
import logging
import random
import MatrixDriver


class TESmartMatrix(MatrixDriver.MatrixDriver):
  def __init__(self, serial_port, name="TESmartMatrix"):
    super().__init__(serial_port, name=name)
    self.serial_port.write(b'MT00RD0000NT')
    
  def process(self, status):
    self.status = str(status)
  
  def getOutput(self, port):
    # LINK:O1I2;O2I2;O3I2;O4I1;O5I2;O6I1;O7I9;O8I2;END
    start = 5+(5*(port-1))
    logging.debug( "port=[%s] part=[%s]" % (port, str(self.status)[start+5]) ) 
    return int(self.status[start+5])

  @staticmethod
  def outputString(outport, inport):
    return b"MT00SW%02d%02dNT"%(inport, outport)

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

