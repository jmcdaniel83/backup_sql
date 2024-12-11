#!/usr/bin/env python
'''
@CUSTOMIZE  Place module documenation here.
'''

__author__ = 'Jason McDaniel'
__copyright__ = 'Copyright 2021'
__credits__ = ['Jason McDaniel']
__license__ = 'Open Source'
__version__ = '0.1.0'
__maintainer__ = 'Jason McDaniel'
__email__ = 'jaymac83@gmail.com.com'
__status__ = 'Prototype'

# standard modules
import logging
import os
import copy
import json

from datetime import datetime
# @CUSTOMIZE  Add standard modules here.

# third-party modules
# @CUSTOMIZE  Add third party modules here.

# custom modules
from common.log import Log
from mysql_db import MySqlConfig, MySqlDbConnector
# @CUSTOMIZE  Add custom modules here.

def save_version_info(config: MySqlConfig, ts: str):
    # copy the configuration for a local version
    new_config = copy.deepcopy(config)
    # update to the world database
    new_config.update_database('world')

    # get our version
    logging.info(f'getting verison info from {config.db}...')
    with MySqlDbConnector(new_config, ts) as conn:
        # get our version info
        version_info = conn.get_version()

        # generate our time stamp for this file
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        version_file = f'version_info_{ts}.json'
        version_file_path = os.path.join(conn.sql_backup_dir, version_file)

        with open(version_file_path, 'w') as fout:
            json.dump(version_info, fout, indent=3)

        return version_info

def main():
    # initialize our timestamp for this run
    ts = datetime.now().strftime('%Y%m%d_%H%M')

    # load our configuration file
    config_file = os.path.join('.', 'mysql_config.json')
    mysql_config = MySqlConfig(config_file)

    # get our version info
    save_version_info(mysql_config, ts)

    # go through each database and backup the instance
    dbs =['auth', 'characters', 'world']
    for db_name in dbs:
        mysql_config.update_database(db_name)

        with MySqlDbConnector(mysql_config, ts) as conn:
            conn.backup()
            pass

    pass

if __name__ == '__main__':
    Log.init()
    main()

#EOF
