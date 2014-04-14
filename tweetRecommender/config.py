from configparser import ConfigParser

CONFIGFILE = "/../conf/application.conf"

filename = os.path.dirname(__file__) + CONFIGFILE
config = ConfigParser()
config.read(filename)
