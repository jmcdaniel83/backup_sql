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
# @CUSTOMIZE  Add standard modules here.

# third-party modules
# @CUSTOMIZE  Add third party modules here.

# custom modules
# @CUSTOMIZE  Add custom modules here.

class Log(object):

   @classmethod
   def init(cls):
      log_dir = os.path.join('.', '_log')
      os.makedirs(log_dir, exist_ok=True)

      log_file_path = os.path.join(log_dir, 'mysql_backup.log')

      # get root logger
      root_logger = logging.getLogger()

      # get the global level
      root_logger.setLevel(logging.INFO)

      # setup file handler
      fh = logging.FileHandler(filename=log_file_path)
      fh.setLevel(logging.DEBUG)

      # setup console handler
      ch = logging.StreamHandler()
      ch.setLevel(logging.INFO)

      # formatter
      formatter = logging.Formatter(
         '{asctime}::{name}::{levelname} - {message}', style='{')
      fh.setFormatter(formatter)
      ch.setFormatter(formatter)

      # add the handlers to our logger
      root_logger.addHandler(fh)
      root_logger.addHandler(ch)

# EOF
