"""
scalemat.py:

This overrides the TESmart driver in order to provide a matrix controller that
is also capable of inserting messages into the serial interface that are
destined to be parsed and removed in-transit. This allows us to send messages
to the scale-switch project using the same serial interface as the Matrix.


@author lestarch
"""
import re
import socket
import time
import uuid

from . import tesmart


class ScaleMatrix(tesmart.TESmartMatrix):
    """
    ScaleMatrix: a class designed to inject messages expected to be removed in-transit.
    Allowing for communication to a device installed as a pass-through on the serial chain.
    """

    MESSAGE_INTERVAL = 4
    KEY_WIDTH = 4
    MSG_WIDTH = 20

    def __init__(self, port, name="ScaleMatrix"):
        """
        Construct basic members and forward the rest to the TESmart setup
        @param port: port string to open up
        @param name: name of the thread
        """
        super().__init__(port, name)
        # TODO: should this be a queue?
        #  In theory this should be safe as the list itself should be consistent
        self.messages = []
        self.lastmsg = time.time()

    def loop(self):
        """
        Runs as part of the thread loop occasionally inserting messages into the data stream.
        """
        super().loop()
        if (time.time() - self.lastmsg) > self.MESSAGE_INTERVAL:
            self.lastmsg = time.time()
            # Send a message if a message is ready
            if self.messages:
                key, msg = self.messages.pop(0)
                # Port defined in parent
                formatter = "<{{:{}.{}}}{{:{}.{}}}>".format(
                    self.KEY_WIDTH, self.KEY_WIDTH, self.MSG_WIDTH, self.MSG_WIDTH
                )
                self.port.write(formatter.format(key, msg).encode("ascii"))
            else:
                self.messages.extend(self.request())

    def error(self, error):
        """
        Queues up an error to send as a message
        :param error: error message
        """
        self.messages.append(("Err", error))

    def request(self):  # pylint: disable=no-self-use
        """
        Request that messages be filled and prepared to be sent.
        Return a list of (key, msg) pairs to be queued
        :return: (key, msg) pairs to send
        """
        # Get the MAC address of the first interface
        mac = ":".join(re.findall("..", hex(uuid.getnode())[2:]))
        # Try to get the best IP address
        ipadd = self.get_ip_address()
        return [
            ("Host", socket.gethostname()),
            ("MAC", mac.upper()),
            ("IP", ipadd),
            (" !! ", "STARCH!!!!!!!!!"),
        ]

    @staticmethod
    def get_ip_address():
        """ Connect to Google's DNS to Read the Public IP"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
        except:
            pass
        try:
            ipadd = socket.gethostbyname(socket.gethostname())
            if ipadd.startswith("127"):
                ipadd = socket.gethostbyname(socket.getfqdn())
            return ipadd
        except:
            pass
        return "No Network?"
