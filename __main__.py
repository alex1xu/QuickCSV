"""
Alex Xu
(alex1xu)
alexxugn@gmail.com

__main__.py
-loads the configs
-loads the trade listings
-starts the GUI
"""

import app
import yaml
import util as util


def load_configs():
    """
    loads the configuration file
    """
    config_stream=open('config.yaml','r')
    configs=yaml.safe_load(config_stream)
    configs['dc']['CSVdtf']=configs['dc']['CSVdf']+'.'+configs['dc']['CSVtf']
    configs['dc']['UIdtf']=configs['dc']['UItf']+' on '+configs['dc']['UIdf']

    return configs


configs=load_configs()

util.CSV.read()

main=app.GUI()