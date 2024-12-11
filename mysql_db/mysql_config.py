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
import json
# @CUSTOMIZE  Add standard modules here.

# third-party modules
# @CUSTOMIZE  Add third party modules here.

# custom modules
# @CUSTOMIZE  Add custom modules here.

class MySqlConfig(object):
   host: str = ''
   user: str = ''
   passwd: str = ''
   db: str = ''
   port: int = 3306
   use_pure: bool = True

   @property
   def as_json(self) -> dict:
      return {
         "host": self.host,
         "user": self.user,
         "passwd": self.passwd,
         "db": self.db,
         "port": self.port,
         "use_pure": self.use_pure
      }

   def __init__(self, file_path: str):
      with open(file_path, 'r') as fin:
         json_data = json.load(fin)
         # associate this object with the provided JSON
         self.__dict__ = json_data

   def update_database(self, db_name: str):
      self.db = db_name

#EOF
