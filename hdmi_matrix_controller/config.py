"""
config.py:

This file contains the configuration for the flask server. It will configure the matrix hardware to use, as well as set
up other basic properties of the system.

@author lestarch
"""
import os

STATIC_FILES_PATH = os.environ.get("STATIC_FILES_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "html-new"))
MATRIX_TYPE = os.environ.get("MATRIX_TYPE", "SCALE_MATRIX")
MATRIX_SERIAL_PORT = os.environ.get("MATRIX_SERIAL_PORT", "/dev/ttyUSB0")
