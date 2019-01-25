"""
TESmart.py:

Module containing TESmart matix driver code, for interacting with the TESmart matrix driver.

@author mproctor13
"""
import copy
import logging
import re
import time

import serial

from . import matrix

# TODO: must fix why pending latches non-assigned values)


class TESmartMatrix(matrix.MatrixDriver):
    """
    TESmartMatrix driver used to drive the TESmart matrix.
    """

    OUT_REG = re.compile(r"O\dI(\d)")

    def __init__(self, port, name="TESmartMatrix"):
        """
        Open up the serial port owning this driver
        @param port: port string to open up
        @param name: name of the thread
        """
        super().__init__(inputs=4, outputs=4, name=name)
        self.port = serial.Serial(port, timeout=11 * 48 / (8 * 9600))
        self.previous = ""

    def setup(self):
        """
        Initial setup for this matrix. Send out the initial write.
        """
        self.port.write(b"MT00RD0000NT")

    def loop(self):
        """https://github.com/socallinuxexpo/hdmi_matrix_control
        Runs one iteration of the loop to process this driver
        """
        # If something has been registered on pending, send out the data
        if self.pending:
            output, value = self.pending.pop(0)
            #if self.channels[output] != value:
            print(f"Output = {output}, Value = {value}")
            self.assign_helper(output, value)
            # Now read back once
            self.port.write(b"MT00RD0000NT")
            time.sleep(0.1)
        raw = self.port.read(48)
        # "self.previous = {raw} ; err1 = {error1} ; err2 = {error2}")
        self.previous += raw.decode("ascii")
        if len(self.previous) >= 48:
            data = self.previous[:48]
            self.previous = self.previous[48:]
            matches = self.OUT_REG.finditer(data)
            self.channels = [int(match.group(1)) - 1 for match in matches][
                : self.outputs
            ]

    def assign_helper(self, out_chan, in_chan):
        """
        Assign a given input channel to a given output channel, for use on main event-loop.
        @param out_chan: output channel
        @param in_chan: input channel
        """
        logging.debug("Assigning %d to %d", out_chan, in_chan)
        assert out_chan < self.outputs, "Invalid output channel %d" % out_chan
        assert in_chan < self.inputs, "Invalid input channel %d" % in_chan
        self.port.write(b"MT00SW%02d%02dNT" % (in_chan + 1, out_chan + 1))
        time.sleep(0.1)
