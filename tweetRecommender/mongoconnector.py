from configparser import ConfigParser
from pymongo import MongoClient
import os

class MongoConnector:

  def __init__(self):
    config_file = os.path.dirname(__file__) + "/../conf/application.conf"
    config = ConfigParser()
    print(os.path.dirname(__file__))
    print(str(config.read(config_file)))

    self.client = MongoClient(config['mongodb']['host'])
    self.client[config['mongodb']['database']].authenticate(config['mongodb']['user'], config['mongodb']['password'])
    self.db = self.client[config['mongodb']['database']]

mongo = MongoConnector()