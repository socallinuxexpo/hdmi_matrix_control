from flask.ext.restful import reqparse
from flask.ext import restful

class Output(restful.Resource):
  def __init__(self):
    self.parser = reqparse.RequestParser()
    self.parser.add_argument("set", type=int, help="Set which input this output should be connected to.")
  def get(self):
    logging.info("set [%s]" % args )
    return 1
  def put(self):
    args = self.parser.parse_args()
    logging.info("set [%s]" % args )
