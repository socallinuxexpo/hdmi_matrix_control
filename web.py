import serial
import time
import threading
import logging
import random
import TESmartMatrix
from flask import Flask, render_template
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

def abort_if_doesnt_exist(port_type, port):
  global driver
  if port.isdigit():
    port_num = int(port)
    if driver.port_exists(port_type, port_num):
      return port_num
  abort(404, message="{} port {} doesn't exist".format(port_type, port))

class OutputPort(Resource):
  def __init__(self):
    self.parser = reqparse.RequestParser()
    self.parser.add_argument('input')
  def get(self, output_port):
    global driver
    oport = abort_if_doesnt_exist("Output", output_port)
    return driver.getOutput(oport)
  def put(self, output_port):
    global driver
    args = self.parser.parse_args()
    logging.debug("Get input=[{}] output=[{}]".format(args,output_port) )
    oport = abort_if_doesnt_exist("Output", output_port)
    iport = abort_if_doesnt_exist("Input", args['input'])
    driver.setOutput(oport, iport)
    return '', 201

class OutputPortList(Resource):
  def get(self):
    global driver
    return driver.toJSON()

api.add_resource(OutputPortList, '/outputs')
api.add_resource(OutputPort, '/output/<output_port>')
@app.route("/")
def index():
  return render_template('index.html', matrix=driver)

#logging.basicConfig(level=logging.DEBUG,
logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-13s)[%(levelname)-8s] %(message)s',
                    )

def flaskTread():
  app.run(use_reloader=False)

if __name__ == "__main__":
  serial_port = serial.Serial('/dev/ttyUSB0')  # open serial port
  logging.debug(serial_port.name)
 
  #driver = MatrixDriver.MatrixDriver(serial_port) 
  driver = TESmartMatrix.TESmartMatrix(serial_port) 
  driver.start()
#  time.sleep(5)  
  logging.warning("This is a warning.")
  logging.error("This is an error.")
  logging.critical("This is a critical.")

  t1 = threading.Thread(target=flaskTread,name="webThread")    
  t1.start()
  t1.join()
  driver.join()

  serial_port.close()

