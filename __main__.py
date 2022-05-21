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
import pandas as pd


def load_configs():
    """
    loads the configuration file
    """
    config_stream=open('config.yaml','r')
    configs=yaml.safe_load(config_stream)
    configs['dc']['CSVdtf']=configs['dc']['CSVdf']+'.'+configs['dc']['CSVtf']
    configs['dc']['UIdtf']=configs['dc']['UItf']+' on '+configs['dc']['UIdf']

    return configs


def load_futures_info():
    """
    loads the futures info file
    """

    futures_info=pd.read_csv(configs['futures_file'],dtype=str)
    return futures_info


configs=load_configs()
futures=load_futures_info()

util.CSV.read()

main=app.GUI()