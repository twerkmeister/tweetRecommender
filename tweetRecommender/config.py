import os.path
from configparser import ConfigParser

CONFIGFILE = "../conf/application.conf"

filename = os.path.join(os.path.dirname(__file__), CONFIGFILE)
config = ConfigParser()
config.read(filename)
