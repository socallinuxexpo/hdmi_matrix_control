'''
TESmart.py:

Module containing TESmart matix driver code, for interacting with the TESmart matrix driver.

@author mproctor13
'''
import re
import time
import logging
import serial

import hw.matrix


class TESmartMatrix(hw.matrix.MatrixDriver):
    '''
    TESmartMatrix driver used to drive the TESmart matrix.
    '''
    OUT_REG = re.compile(r"O\dI(\d)")
    def __init__(self, port, name="TESmartMatrix"):
        '''
        Open up the serial port owning this driver
        @param port: port string to open up
        @param name: name of the thread
        '''
        super().__init__(inputs=4, outputs=4, name=name)
        self.port = serial.Serial(port)

    def setup(self):
        '''
        Initial setup for this matrix. Send out the initial write.
        '''
        self.port.write(b'MT00RD0000NT')

    def loop(self):
        '''
        Runs one iteration of the loop to process this driver
        '''
        data = self.port.read(48)
        if len(data) == 48:
            data = str(data)
            matches = self.OUT_REG.finditer(data)
            self.channels = [int(match.group(1)) - 1 for match in matches][:self.outputs]
            print("Chans:", self.channels)
        else:
            logging.warning("Unexpected message: %s", data)
        super().loop()

    def assign(self, out_chan, in_chan):
        '''
        Assign a given input channel to a given output channel
        @param out_chan: output channel
        @param in_chan: input channel
        '''
        print("Assigning %d to %s", out_chan, in_chan)
        assert out_chan < self.outputs, "Invalid output channel %d" % out_chan
        assert in_chan < self.inputs, "Invalid input channel %d" % in_chan
        self.port.write(b"MT00SW%02d%02dNT" % (in_chan + 1, out_chan + 1))
        time.sleep(0.1)
        self.port.write(b'MT00RD0000NT')
        time.sleep(0.1)
