"""
hdmi_matrix_control.web:

This is the REST API that allows control of the HDMI matrix
over the Internet.

The following endpoints and HTTP verbs are allowed:
GET /inputs: Returns list of inputs, as JSON.
GET /outputs: Returns output map to inputs
GET /output/<portnum>: Returns the input port associated with an output port.
PUT /output/<portnum>: Sets the input port associated with an output port.
                       The data format is "input=<portnum>".

Port numbers must be between 1 and n, where n is the driver's maximum number
of input or output ports.
"""
import os


import logging

from flask import Flask, render_template
from flask_restful import Api, Resource, abort, reqparse

from . import driver

STATIC_FILES = os.path.join(os.path.dirname(__file__),  "..", "..", "html-new")
APP = Flask(__name__, static_folder=STATIC_FILES)
API = Api(APP)


def abort_if_doesnt_exist(port_type, port):
    """
    Checks if an input or output port is a valid port of the driver.
    Returns a 404 response if it does not exist.
    """
    if port.isdigit():
        port_num = int(port)
        if driver.DRIVER.port_exists(port_type, port_num - 1):
            return port_num

    abort(404, message="{} port {} doesn't exist".format(port_type, port))
    return None


class OutputPort(Resource):
    """
    Resource hat handles the URL for a assigning and reading
    a single output port.
    """
    def __init__(self):
        """
        Constructor creates a request parser to check PUT data.
        """
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("input")

    def get(self, output_port):  # pylint: disable=no-self-use
        """
        Returns the input port associated with an output port.
        """
        oport = abort_if_doesnt_exist("Output", output_port)
        return driver.DRIVER.read(oport - 1) + 1

    def put(self, output_port):
        """
        Sends an output/input pair to the driver to be assigned.
        Returns a 201 response if successful.
        """
        args = self.parser.parse_args()
        logging.debug("Get input=[%s] output=[%s]", args, output_port)
        oport = abort_if_doesnt_exist("Output", output_port)
        iport = abort_if_doesnt_exist("Input", args["input"])
        driver.DRIVER.assign(oport - 1, iport - 1)
        return "", 201


class OutputPortList(Resource):
    """
    Resource that handles the URL for reading all
    ports of the driver.
    """
    def get(self):  # pylint: disable=no-self-use
        """
        Returns the JSON representation of the driver.
        """
        logging.info(driver.DRIVER.to_json())
        return driver.DRIVER.to_json()



class InputPort(Resource):
    """
    Resource hat handles the URL for a assigning and reading
    a single output port.
    """

    def get(self):  # pylint: disable=no-self-use
        """
        Returns the input port associated with an output port.
        """
        return [1, 2, 3, 4]


API.add_resource(InputPort, "/matrix/inputs")
API.add_resource(OutputPortList, "/matrix/outputs")
API.add_resource(OutputPort, "/matrix/output/<output_port>")

@APP.route('/<path:path>')
def send_static_files(path):
    return APP.send_static_file(path)


@APP.route("/")
def index():
    """
    Renders demo web page.
    """
    return APP.send_static_file("yeet.html")


def flask_thread():
    """
    Starts the Flask app.
    """
    APP.run(use_reloader=False)
