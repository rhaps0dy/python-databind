
__author__ = 'Niklas Rosenstein <rosensteinniklas@gmail.com>'
__version__ = '0.0.0'

from ._plugin import DatabindPlugin


def plugin(version: str):
  return DatabindPlugin