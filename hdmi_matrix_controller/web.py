""" hdmi_matrix_controller.web """
# pylint: disable=missing-docstring
# TODO: Add docstrings to module
import logging

from flask import Flask, render_template
from flask_restful import Api, Resource, abort, reqparse

from . import driver


APP = Flask(__name__)
API = Api(APP)


def abort_if_doesnt_exist(port_type, port):
    if port.isdigit():
        port_num = int(port)
        if driver.DRIVER.port_exists(port_type, port_num):
            return port_num
    abort(404, message="{} port {} doesn't exist".format(port_type, port))


class OutputPort(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("input")

    def get(self, output_port):
        oport = abort_if_doesnt_exist("Output", output_port)
        return driver.DRIVER.getOutput(oport)

    def put(self, output_port):
        args = self.parser.parse_args()
        logging.debug("Get input=[%s] output=[%s]", args, output_port)
        oport = abort_if_doesnt_exist("Output", output_port)
        iport = abort_if_doesnt_exist("Input", args["input"])
        driver.DRIVER.setOutput(oport, iport)
        return "", 201


class OutputPortList(Resource):
    def get(self):
        return driver.DRIVER.toJSON()


API.add_resource(OutputPortList, "/outputs")
API.add_resource(OutputPort, "/output/<output_port>")


@APP.route("/")
def index():
    return render_template("index.html", matrix=driver.DRIVER)


def flask_thread():
    APP.run(use_reloader=False)
