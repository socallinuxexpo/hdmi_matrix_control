""" Package HDMI Matrix Controller top level """
import logging

import pkg_resources


try:
    __version__ = pkg_resources.get_distribution(__name__).version
except pkg_resources.DistributionNotFound:
    __version__ = None

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = ["hw"]
