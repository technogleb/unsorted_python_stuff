"""
Context manager to work with postgresql python adapter (psycopg2).

Usage example:
--------------
>>> db = DatabaseHandler(user='user', password='password', server='host', database='postgres')
with db:
    res = db.execute(sql, params)
    for row in res:
        do_something(row)
"""

import getpass
import psycopg2
from psycopg2 import extras


class DatabaseHandler:
    """
    Context manager, that helps your write a little bit less code
    when working with psycopg2
    """
    def __init__(self, user='postgres', password='postgres',
                 server='ipv4', database='postgres'):
        self.user = user
        self._password = password
        self.server = server
        self.database = database
        self.conn = None
        self.cursor = None

    def execute(self, sql, params=None):
        """Executes sql query here"""
        self.cursor.execute(sql, params)
        return self.cursor

    @property
    def password(self):
        if self._password == 'postgres':
            return self._password
        return getpass.getpass("Enter password for {}: ".format(self.user))

    def __enter__(self):
        self.conn = psycopg2.connect(
            host=self.server,
            user=self.user,
            password=self.password,
            dbname=self.database
        )
        self.cursor = self.conn.cursor(
            'named cursor', cursor_factory=extras.RealDictCursor)
        return self

    def __exit__(self, type, values, traceback):
        self.conn.close()
        self.cursor.close()
