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

from datetime import datetime
# @CUSTOMIZE  Add standard modules here.

# third-party modules
from mysql.connector import MySQLConnection, connect, Error
from mysql.connector.cursor import MySQLCursor
# @CUSTOMIZE  Add third party modules here.

# custom modules
from mysql_db.mysql_config import MySqlConfig
# @CUSTOMIZE  Add custom modules here.

class MySqlDbConnector(object):

   __VERSION_QUERY = 'select * from `version`;'

   _config: MySqlConfig
   _db: MySQLConnection
   _cursor: MySQLCursor
   _ts: str

   @property
   def host_name(self) -> str:
      return self._config.host

   @property
   def port(self) -> int:
      return self._config.port

   @property
   def database_name(self) -> str:
      return self._config.db

   @property
   def sql_backup_dir(self) -> str:
      backup_dir = os.path.join('.', 'sql', 'backup', self._ts)
      os.makedirs(backup_dir, exist_ok=True)
      return backup_dir

   def __init__(self, config: MySqlConfig, ts: str):
      # intialize our timestamp for this connection
      self._ts = ts

      # save our items
      self._config = config
      # default values for the database objects
      self._db = MySQLConnection()
      self._cursor = MySQLCursor()

   def get_version(self):
      # only works on 'world' database
      if self.database_name != 'world':
         logging.warning(f'version information must come from [world] database not [{self.database_name}]')
         return None

      # get our version data
      result = self._query_fetchone(self.__VERSION_QUERY)
      return result

   def backup(self):
      ## backup the currently defined database
      # generate our backup file name
      ts = datetime.now().strftime('%Y%m%d_%H%M%s')
      file_name = f'{self.database_name}-{ts}.sql'
      file_path = os.path.join(self.sql_backup_dir, file_name)

      dump_cmd = f'mysqldump --hex-blob --add-drop-trigger -h {self.host_name} --port {self.port} -u {self._config.user} -p{self._config.passwd} {self.database_name}'
      command = f'{dump_cmd} > {file_path}'
      logging.info(f'backing up {self.database_name}...')
      logging.debug(f'running command:\n\t{command}')
      os.system(command)
      logging.info(f'database {self.database_name} saved!')

   def __enter__(self):
      # establish our connection
      logging.info(f'connecting to [{self.database_name}] {self.host_name}:{self.port}...')
      self._connect(self._config.as_json)
      return self

   def __exit__(self, *exc):
      # close our connection
      logging.info(f'closing connection to {self.host_name}...')
      self._cursor.close()
      self._db.close()
      return False

   def _connect(self, config: dict):
      try:
         self._db = connect(**config) # type: ignore
         self._cursor = self._db.cursor(dictionary=True)
      except Error as ex:
         logging.error(f'issue trying to connect to db: {ex}')

   def _query_fetchone(self, query: str, params: tuple=None):
      self._query(query, params)
      result = self._cursor.fetchone()
      return result

   def _query_fetchall(self, query: str, params: tuple=None):
      self._query(query, params)
      result = self._cursor.fetchall()
      return result

   def _query(self, query: str, params: tuple=None):
      # execute our query
      try:
         self._cursor.execute(query, params)
      except Error as ex:
         logging.error(f'issue occured during query: {ex}')

#EOF
