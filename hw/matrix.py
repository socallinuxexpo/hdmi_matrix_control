'''
MatrixDriver:

Contains the root functionality for the matrix driver and related components.

@author mproctor13
'''
import time
import threading
import logging
import random
import simplejson as json
from time import sleep

class MatrixDriver(threading.Thread):
  '''
  Base class of the matrix driver component. Provides a running thread and basic interactivity
  for generic matrix switches.
  '''
  def __init__(self, inputs=4, outputs=4, name="MatrixDriver"):
    '''
    Construct the matirx driver and associated thread.
    @param inputs: number of inputs
    @param outputs: number of outputs
    @param name: name to provide the thread
    '''
    threading.Thread.__init__(self, name=name)
    self.inputs = inputs
    self.outputs = outputs
    #inputs and output checks
    assert inputs >= 1, "Expected integral number of inputs"
    assert outputs >= 1, "Expected integral number of outputs"
    self.channels = [1] *  outputs #All inputs start mapped to 1

  def setup():
    '''
    Setup function.
    '''
    logging.debug("Setting up Matrix")

  def assign(out_chan, in_chan):
    '''
    Assign a given input channel to a given output channel
    @param out_chan: output channel
    @param in_chan: input channel
    '''
    logging.debug("Assigning %d to %s", (out_chan, in_chan))
    assert out_chan < self.outputs, "Invalid output channel %d" % out_chan
    assert in_chan < self.inputs, "Invalid input channel %d" % in_chan
    self.channels[out_chan] = in_chan

  def read(out_chan):
    '''
    Reads what a current output is set to.
    @param out_chan: output channel to read
    '''
    logging.debug("Request to read %d", out_chan)
    assert out_chan < self.outputs, "Invalid output channel %d" % out_chan
    return self.channels[out_chan]

  def loop(self):
    '''
    Run one loop iteration
    '''
    logging.debug("Iterating loop")

  def run(self):
    '''
    Main thread/looping function
    '''
    self.setup()
    while self.running:
      self.loop()
      self.sleep(0.1)

#  def toJSON(self):
#    test = {}
#    test['name'] = self.name
#    test['config'] = {}
#    test['config']['inputs'] = self.num_inputs
#    test['config']['outputs'] = self.num_outputs
#    test['outputs'] = {}
#    for output in range(1, self.num_outputs+1):
#      test['outputs']["output_{}".format(output)] = self.getOutput(output)
#    return json.dumps(test, sort_keys=True)

#if __name__ == "__main__":
#  serial_port = '/dev/ttyUSB0'
#  mat = MatrixDriver(serial_port)
#  print( mat.toJSON() )

