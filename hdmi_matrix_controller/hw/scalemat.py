"""
scalemat.py:

This overrides the TESmart driver in order to provide a matrix controller that is also capable of inserting messages
into the serial interface that are destined to be parsed and removed in-transit. This allows us to send messages to
the scale-switch project using the same serial interface as the Matrix.


@author lestarch
"""
import re
import socket
import time
import uuid

from . import tesmart


class ScaleMatrix(tesmart.TESmartMatrix):
    """
    ScaleMatrix: a class designed to inject messages expeced to be removed in-transit. Allowing for communication to
    a device installed as a pass-through on the serial chain.
    """
    MESSAGE_INTERVAL = 10
    KEY_WIDTH = 4
    MSG_WIDTH = 20

    def __init__(self, port, name="ScaleMatrix"):
        """
        Construct basic members and forward the rest to the TESmart setup
        @param port: port string to open up
        @param name: name of the thread
        """
        super().__init__(port, name)
        # TODO: should this be a queue? In theory this should be safe as the list itself should be consistent
        self.messages = []
        self.last = time.time()

    def loop(self):
        """
        Runs as part of the thread loop occasionally inserting messages into the data stream.
        """
        super().loop()
        if (time.time() - self.last) > self.MESSAGE_INTERVAL:
            # Send a message if a message is ready
            if self.messages:
                key, msg = self.messages.pop(0)
                # Port defined in parent
                formatter = "<{{:{}.{}}}:{{:{}.{}}}>".format(self.KEY_WIDTH, self.KEY_WIDTH,
                                                             self.MSG_WIDTH, self.MSG_WIDTH)
                self.port.write(formatter.format(key, msg).encode("ascii"))
            else:
                self.messages.extend(self.request())

    def error(self, error):
        """
        Queues up an error to send as a message
        :param error: error message
        """
        self.messages.append(("Err", error))

    def request(self):
        """
        Request that messages be filled and prepared to be sent. Return a list of (key, msg) pairs to be queued
        :return: (key, msg) pairs to send
        """
        # Get the MAC address of the first interface
        mac = ":".join(re.findall("..", hex(uuid.getnode())[2:]))
        # Try to get the best IP address
        ipadd = socket.gethostbyname(socket.gethostname())
        if ipadd.startswith("127"):
            ipadd = socket.gethostbyname(socket.getfqdn())
        return [("Host", socket.gethostname()),
                ("MAC", mac),
                ("IP", ipadd),
                (" !! ", "STARCH!!!!!!!!!")]
