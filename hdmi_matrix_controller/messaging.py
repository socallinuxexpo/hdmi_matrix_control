"""
messaging:

This holds the functionality of the messaging layer for the Matrix switch. Currently this is implemented using ZeroMQ as
a messaging layer.  It supports the following JSON based functions:

 - send: sends a command or reply over the pipe
 - recv: receives a command or reply from the pipe

@author lestarch
"""
import zmq

import logging
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("zmq-msq")

CONNECTION_STRING = "ipc:///tmp/matrix"

context = zmq.Context()
active = None

# Messaging exception is merely an alias
MessagingException = zmq.ZMQError


def _setup(type):
    """
    Sets up the messaging active handler using type.  This is intended to be an internal function.
    :param type: zmq.REQ, or zmq.REP
    """
    global active
    if active is not None:
        close()
    assert active is None, "Already setup, cannot setup again"
    assert type == zmq.REQ or type == zmq.REP, "Invalid type to setup"
    active = context.socket(type)
    LOGGER.debug("Attempting ZMQ %s socket", ("REQ" if type == zmq.REQ else "REP"))
    # Connect or bind depending on type
    if type == zmq.REQ:
        active.connect(CONNECTION_STRING)
    else:
        active.bind(CONNECTION_STRING)
    LOGGER.info("Created ZMQ %s socket", ("REQ" if type == zmq.REQ else "REP"))


def setup_request():
    """
    Setup the request handler for the messaging layer. This will allow other portions of this module to function as
    expected.
    """
    _setup(zmq.REQ)


def setup_reply():
    """
    Setup the reply handler for the messaging layer. This will allow other portions of this module to function as
    expected.
    """
    _setup(zmq.REP)


def send(object):
    """
    Sends an object in JSON format.
    """
    assert active is not None, "Messaging is not setup."
    LOGGER.info("Sending ZMQ message: %s", object)
    active.send_json(object)
    LOGGER.debug("Sent ZMQ message successfully")


def recv():
    """
    Receives the incomming JSON object.
    :return:  python onject.
    """
    assert active is not None, "Messaging is not setup."
    LOGGER.debug("Attempting to receive ZMQ message")
    message = active.recv_json()
    LOGGER.info("Received ZMQ message: %s", message)
    return message


def send_recv(command, retries=3):
    """
    Sends a command and receives a response immediately.  If there is a crash, the socket will be reset. Note: this is
    a blocking operation, so it should not be run in time sensitive contexts, unless it is believed that the request
    will return promptly. This is mostly a helper for send/recv clients
    :param command: command to send
    :return: response to get
    """
    last_exc = None
    for retry in range(0, retries):
        try:
            send(command)
            return recv()
        except MessagingException as mxc:
            LOGGER.warning("Failed to send message and recv response. Retrying. Error: %S", mxc)
            setup_request()
            last_exc = mxc
    # Raise the last exception encountered
    else:
        LOGGER.critical("Failed to send message and recv response. Error: %S", last_exc)
        raise last_exc from None



def close():
    """
    Closes the socket, in preparation to try-again
    """
    global active
    assert active is not None, "Messaging not setup"
    LOGGER.info("Closing ZMQ socket")
    active.close()
    LOGGER.debug("Closed ZMQ socket successfully")
    active = None
