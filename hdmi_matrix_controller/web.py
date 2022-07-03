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
import logging
import subprocess
from pathlib import Path
import flask
import flask_restful
import  flask_restful.reqparse

from . import config
from . import messaging

# Create the flask app, and load configuration from the object
app = flask.Flask(__name__)
app.config.from_object('hdmi_matrix_controller.config')
app.static_folder = app.config["STATIC_FILES_PATH"]

# Configure restful API
api = flask_restful.Api(app)
messaging.setup_request()
geometry = {key: value for key, value in messaging.send_recv({"command": "read"}).items()}

BIN_DIR = Path(__file__).parent.parent.parent / "bin"
assert BIN_DIR.exists(), "Could not find binary directory"

def get_valid_port(port, ptype):
    """
    Gets a valid port number for the matix. If the supplied port is not a number, or that number is out of range, then
    this will abort with a 404 error. Otherwise a valid port number is returned.
    """
    message = "No error, at least I didn't think so"
    try:
        port = int(port , 0)
        prange = geometry[ptype+"s"]
        assert 0 <= port < prange, "{} port {} not in [0, {})".format(ptype, port, prange)
        return port
    except (ValueError, TypeError) as vte:
        message = "{} is not a valid integer".format(port)
    except KeyError as ker:
        message = "{} is not a valid port type".format(ker)
    except AssertionError as ase:
        message = str(ase)
    flask_restful.abort(404, message=message)
    return None


class OutputPort(flask_restful.Resource):
    """
    Resource hat handles the URL for a assigning and reading
    a single output port.
    """
    def __init__(self):
        """
        Constructor creates a request parser to check PUT data.
        """
        self.parser = flask_restful.reqparse.RequestParser()
        self.parser.add_argument("input")

    def get(self, output_port):  # pylint: disable=no-self-use
        """
        Returns the input port associated with an output port.
        """
        output_port = get_valid_port(output_port, "output")
        return messaging.send_recv({"command": "read"})["channels"][output_port], 200

    def put(self, output_port):
        """
        Sends an output/input pair to the driver to be assigned.
        Returns a 201 response if successful.
        """
        args = self.parser.parse_args()
        logging.debug("Get input=[%s] output=[%s]", args, output_port)
        output_port = get_valid_port(output_port, "output")
        input_port = get_valid_port(args["input"], "input")
        return messaging.send_recv({"command": "assign", "output":output_port, "input": input_port})


class OutputPortList(flask_restful.Resource):
    """
    Resource that handles the URL for reading all
    ports of the driver.
    """
    def get(self):  # pylint: disable=no-self-use
        """
        Returns the JSON representation of the driver.
        """
        return geometry["outputs"]



class InputPort(flask_restful.Resource):
    """
    Resource hat handles the URL for a assigning and reading
    a single output port.
    """

    def get(self):  # pylint: disable=no-self-use
        """
        Returns the input port associated with an output port.
        """
        return geometry["inputs"]


class Stream(flask_restful.Resource):
    """
    Handles the room streaming implementations.

    GET: what is streaming, or '' if nothing is streaming
    PUT: start a stream with given room
    DELETE: stop streaming
    """
    def __init__(self):
        """
        Constructor creates a request parser to check PUT data.
        """
        self.stream = None
        self.parser = flask_restful.reqparse.RequestParser()
        self.parser.add_argument("stream")

    def get(self):  # pylint: disable=no-self-use
        """
        Returns the currently active stream or ''
        """
        return self.stream if self.stream else "", 200

    def put(self):
        """
        Starts streaming. If already streaming, then stops before starting
        Returns a 201 response if successful, else 500
        """
        if self.stream:
            _, _ = self.delete()
        args = self.parser.parse_args()
        self.stream = args["stream"]
        stream_uri = f"rtmp://{ self.stream }.scaleav.us:1935/scale/mixed"
        logging.debug("Start stream=[%s]", stream_uri)
        process_spec = subprocess.run([BIN_DIR / "start-stream-gst", stream_uri])
        return stream_uri, 200 if process_spec.returncode == 0 else 500

    def delete(self):
        """
        Stops the stream.
        """
        self.stream = None
        process_spec = subprocess.run([BIN_DIR / "stop-stream"])
        return "", 200 if process_spec.returncode == 0 else 500


api.add_resource(InputPort, "/matrix/inputs")
api.add_resource(OutputPortList, "/matrix/outputs")
api.add_resource(OutputPort, "/matrix/output/<output_port>")
api.add_resource(Stream, "/matrix/stream")

@app.route('/<path:path>')
def send_static_files(path):
    return app.send_static_file(path)


@app.route("/")
def index():
    """
    Renders demo web page.
    """
    return app.send_static_file("yeet.html")


def flask_thread():
    """
    Starts the Flask app.
    """
    app.run(use_reloader=False)

