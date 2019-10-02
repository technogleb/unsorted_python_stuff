"""Context manager to work with postgresql python adapter (psycopg2)."""
import os
import psycopg2
from psycopg2 import extras, sql
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
    def __init__(self, user='', password='', host='', dbname=''):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.conn = None
        self.cursor = None

    def execute(self, sql_string, params=None):
        sql_obj = sql.SQL(sql_string)
        self.cursor.execute(sql_obj, params)
        return self.cursor

    @property
    def host(self):
        return self._host

    @property
    def dbname(self):
        return self._dbname

    @property
    def user(self):
        return self._user

    @property
    def password(self):

        return self._password

    @host.setter
    def host(self, signature_host):
        gp_host = os.getenv('POSTGRES_HOST')
        if gp_host:
            self._host = gp_host
        elif signature_host:
            self._host = signature_host
        else:
            self._host = input("Enter postgres hostname or ip: ")

    @dbname.setter
    def dbname(self, signature_dbname):
        gp_dbname = os.getenv('POSTGRES_DBNAME')
        if gp_dbname:
            self._dbname = gp_dbname
        elif signature_dbname:
            self._dbname = signature_dbname
        else:
            self._dbname = input("Enter postgres dbname: ")

    @user.setter
    def user(self, signature_user):
        gp_user = os.getenv('POSTGRES_USER')
        if gp_user:
            self._user = gp_user
        elif signature_user:
            self._user = signature_user
        else:
            self._user = input("Enter postgres username: ")

    @password.setter
    def password(self, signature_password):
        gp_pass = os.getenv('POSTGRES_PASSWORD')
        if gp_pass:
            self._password = gp_pass
        elif signature_password:
            self._password = signature_password
        else:
            self._password = getpass.getpass(
                "Enter password for {}: ".format(self.user))

    def __enter__(self):
        self.conn = psycopg2.connect(
            host=self.host,
            dbname=self.dbname,
            user=self.user,
            password=self.password,
        )
        self.cursor = self.conn.cursor(
            'named cursor', cursor_factory=extras.RealDictCursor)
        return self

    def __exit__(self, type, values, traceback):
        self.conn.close()
        self.cursor.close()
