import time
import threading
import logging
import random
import simplejson as json

class MatrixDriver(threading.Thread):
  running = True
  def __init__(self, serial_port, num_inputs=4, num_outputs=4, name="MatrixDriver"):
    threading.Thread.__init__(self, name=name)
    self.serial_port = serial_port
    self.num_inputs=4
    self.num_outputs=4
    self.status = [0,random.randint(1, 5), random.randint(1, 5), random.randint(1, 5), random.randint(1, 5)]
  def process(self, statusStr):
    logging.debug("process got [%s]" % statusStr)
  def getOutput(self, port):
    logging.debug("getOutput asked about %s" % port)
    return self.status[port]
  def setOutput(self, outport, inport):
     logging.debug( "setOutput got set %s to %s" % (outport, inport) )
  def run(self):
    logging.debug( "Run loop starting." )
    while self.running:
      logging.debug( "Start of loop" )
      t = self.serial_port.read(48)
      if len(t) == 48:
        self.process(t)
        logging.info( "[" + str(self.getOutput(1)) + "] [" + 
		      str(self.getOutput(2)) + "] [" + str(self.getOutput(3)) + "] [" + str(self.getOutput(4)) + "]" )
      else:
        logging.info( t )
      logging.debug( "End of loop" )
  def port_exists(self, port_type, port_num):
    if port_type.lower() == "input":
      if port_num in range(1, self.num_inputs+1):
        return True
    if port_type.lower() == "output":
      if port_num in range(1, self.num_outputs+1):
        return True
    return False
  def countUp(self):
    self.setOutput(1, 1)
    self.setOutput(2, 2)
    self.setOutput(3, 3)
    self.setOutput(4, 4)

  def scan(self):
    logging.debug("write thread starting")
    while 1:
      for outport in range(1, 5):
        inport = self.getOutput(outport)+1
        if inport > 4:
          inport = 1
        self.setOutput(outport, inport)
        time.sleep(1)
  def toJSON(self):
    test = {}
    test['name'] = self.name
    test['config'] = {}
    test['config']['inputs'] = self.num_inputs
    test['config']['outputs'] = self.num_outputs
    test['outputs'] = {}
    for output in range(1, self.num_outputs+1):
      test['outputs']["output_{}".format(output)] = self.getOutput(output)
    return json.dumps(test, sort_keys=True)

if __name__ == "__main__":
  serial_port = '/dev/ttyUSB0'
  mat = MatrixDriver(serial_port)
  print( mat.toJSON() )

