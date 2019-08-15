"""Context manager to work with postgresql python adapter (psycopg2)."""

import psycopg2
from psycopg2 import extras
import getpass


class DatabaseHandler:
    """
    Just a simple postgres manager built as context manager for ease of use,
    that simultaneously opens/closes both connection and cursor.
    Also uses dict cursor.

    Usage example:
    --------------
    >>> db = DatabaseHandler(
    ...        user='user', password='password', server='host', database='postgres')
    >>> sql = "select * from table where timestamp < %s and timestamp > %s"
    >>> params = ('2019-06-03', '2019-06-01')
    >>> def do_something(row):
    ...     print(row['field'])
    >>> with db:
    ...     res = db.execute(sql, params)
    ...     for row in res:
    ...         do_something(row)
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
