"""
MatrixDriver:

Contains the root functionality for the matrix driver and related components.

@author mproctor13
"""
import logging
import threading
import time


class MatrixDriver(threading.Thread):
    """
    Base class of the matrix driver component. Provides a running thread and basic interactivity
    for generic matrix switches.
    """

    def __init__(self, inputs=4, outputs=4, name="MatrixDriver"):
        """
        Construct the matirx driver and associated thread.
        @param inputs: number of inputs
        @param outputs: number of outputs
        @param name: name to provide the thread
        """
        threading.Thread.__init__(self, name=name)
        self.inputs = inputs
        self.outputs = outputs
        # inputs and output checks
        assert inputs >= 1, "Expected integral number of inputs"
        assert outputs >= 1, "Expected integral number of outputs"
        self.channels = [0] * outputs  # All inputs start mapped to 1
        self.pending = []
        self.running = True

    def assign(self, out_chan, in_chan):
        """
        Save a given output and input channel in the list of pending assignments.
        @param out_chan: output channel
        @param in_chan: input channel
        """
        logging.debug("Assigning %d to %d", out_chan, in_chan)
        assert out_chan < self.outputs, "Invalid output channel %d" % out_chan
        assert in_chan < self.inputs, "Invalid input channel %d" % in_chan
        self.pending.append((out_chan, in_chan))

    def read(self, out_chan):
        """
        Reads what a current output is set to.
        @param out_chan: output channel to read
        """
        logging.debug("Request to read %d", out_chan)
        assert out_chan < self.outputs, "Invalid output channel %d" % out_chan
        return self.channels[out_chan]

    def loop(self):
        """
        Run one loop iteration
        """
        logging.debug("Iterating loop")
        for output, in_chan in self.pending:
            self.channels[output] = in_chan
        self.pending = []

    def port_exists(self, port_type, portnum):  # pylint: disable=missing-docstring
        """
        Checks if the specified port exists.
        """
        if port_type == "Input":  # pylint: disable=no-else-return
            return portnum >= 0 and portnum < self.inputs
        elif port_type == "Output":
            return portnum >= 0 and portnum < self.outputs

        logging.debug("Invalid port type %s", port_type)
        return False

    def run(self):
        """
        Main thread/looping function
        """
        logging.debug("Setting up Matrix")
        while self.running:
            self.loop()
            time.sleep(0.1)
