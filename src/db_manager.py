"""
Module to manage database connection and operation
"""
import warnings
import os
import pyodbc


class DBManager:
    """
    A class for managing the database connection and operations.
    """
    DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

    def __init__(self):
        """
        Initializes a new instance of the DBManager class.
        """
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
        """
        Gets the database connection.
        """
        return self._conn

    @property
    def cursor(self):
        """
        Gets the database cursor.
        """
        return self._cursor

    def commit(self):
        """
        Commits the current transaction.
        """
        self.connection.commit()

    def close(self, commit=True):
        """
        Closes the database connection.
        """
        if commit:
            self.commit()
        self.connection.close()

