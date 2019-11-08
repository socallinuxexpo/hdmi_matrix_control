"""
daemon.py:

Takes ownership of a Matrix switch, and receives communications dictating what it should do to the matrix switch. By
separating out this layer, the Flask threading/instance problem is effectively removed, as the daemon will support 0-N
clients and owns exactly one matrix switch in perpetuity.

@author lestarch
"""
from . import config
from . import messaging

import hdmi_matrix_controller.hw.matrix
import hdmi_matrix_controller.hw.tesmart
import hdmi_matrix_controller.hw.scalemat

# Gather configuration to create Matrix driver
if config.MATRIX_TYPE == "SCALE_MATRIX":
    MATRIX = hdmi_matrix_controller.hw.scalemat.ScaleMatrix(config.MATRIX_SERIAL_PORT)
elif config.MATRIX_TYPE == "TESMART_MATRIX":
    MATRIX = hdmi_matrix_controller.hw.tesmart.TESmartMatrix(config.MATRIX_SERIAL_PORT)
elif config.MATRIX_TYPE == "TEST_MATRIX":
    MATRIX = hdmi_matrix_controller.hw.matrix.MatrixDriver()
else:
    raise Exception("Invalid matrix type: {}".format(config.MATRIX_TYPE))


def process_command(command):
    """
    Processes a given command, and returns a result. These commands will be routed to the Matrix at some point.
    :param command: command to process
    :return:
    """
    if command["command"] == "assign":
        MATRIX.assign(command["output"], command["input"])
        return {"reply": "ack"}
    elif command["command"] == "read":
        return MATRIX.to_json()


def main():
    """Hi Lewis!!!"""
    abort = False
    # Start the Matrix switch's internal thread
    MATRIX.start()
    # Setup the messaging layer to respond to requests
    messaging.setup_reply()
    # Go into a command processing loop
    while not abort:
        command = messaging.recv()
        messaging.send(process_command(command))

if __name__ == "__main__":
    main()