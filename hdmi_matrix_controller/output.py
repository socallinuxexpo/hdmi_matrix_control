import logging

from flask_restful import Resource, reqparse


class Output(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "set", type=int, help="Set which input this output should be connected to."
        )

    def get(self):
        logging.info("set [%s]", args)
        return 1

    def put(self):
        args = self.parser.parse_args()
        logging.info("set [%s]", args)
