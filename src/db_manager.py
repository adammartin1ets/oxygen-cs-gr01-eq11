import warnings
import pyodbc
import os


class DBManager:

    DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

    def __init__(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        print("connection attempt")
        self._conn = pyodbc.connect(self.DB_CONNECTION_STRING)
        self._cursor = self._conn.cursor()
        print("connection successful")

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()




