import serial
import time
import threading
import logging
import random
import argparse
import MatrixDriver
import TESmartMatrix
from flask import Flask, render_template
from flask_restful import reqparse, abort, Api, Resource
import driver

app = Flask(__name__)
api = Api(app)

def abort_if_doesnt_exist(port_type, port):
  if port.isdigit():
    port_num = int(port)
    if driver.driver.port_exists(port_type, port_num):
      return port_num
  abort(404, message="{} port {} doesn't exist".format(port_type, port))

class OutputPort(Resource):
  def __init__(self):
    self.parser = reqparse.RequestParser()
    self.parser.add_argument('input')
  def get(self, output_port):
    oport = abort_if_doesnt_exist("Output", output_port)
    return driver.driver.getOutput(oport)
  def put(self, output_port):
    args = self.parser.parse_args()
    logging.debug("Get input=[{}] output=[{}]".format(args,output_port) )
    oport = abort_if_doesnt_exist("Output", output_port)
    iport = abort_if_doesnt_exist("Input", args['input'])
    driver.driver.setOutput(oport, iport)
    return '', 201

class OutputPortList(Resource):
  def get(self):
    return driver.driver.toJSON()

api.add_resource(OutputPortList, '/outputs')
api.add_resource(OutputPort, '/output/<output_port>')
@app.route("/")
def index():
  return render_template('index.html', matrix=driver.driver)


def flaskTread():
  app.run(use_reloader=False)

