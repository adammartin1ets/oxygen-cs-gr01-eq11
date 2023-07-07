import time
import logging
import json
from datetime import datetime
import requests
from signalrcore.hub_connection_builder import HubConnectionBuilder
import warnings
import os
import pyodbc


class UndefinedTokenValue(Exception):
    def __init__(self, default_value):
        message = f"A token value has not been defined, default value returned: {default_value}"
        super().__init__(message)


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


class Main:
    def __init__(self):
        self._hub_connection = None
        self.host = os.getenv("HOST")
        self.token = os.getenv("TOKEN")

        if self.token == 'TokenDefaultValue':
            raise UndefinedTokenValue(default_value='TokenDefaultValue')

        self.tickets = os.getenv("TICKETS")
        self.t_max = os.getenv("T_MAX")
        self.t_min = os.getenv("T_MIN")

    def __del__(self):
        if self._hub_connection is not None:
            self._hub_connection.stop()

    def setup(self):
        self.set_sensor_hub()

    def start(self):
        self.setup()
        self._hub_connection.start()

        print("Press CTRL+C to exit.")
        while True:
            time.sleep(2)

    def set_sensor_hub(self):
        print("Attempting connection...")
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.host}/SensorHub?token={self.token}")
            .configure_logging(logging.INFO)
            .with_automatic_reconnect(
                {
                    "type": "raw",
                    "keep_alive_interval": 10,
                    "reconnect_interval": 5,
                    "max_attempts": 999,
                }
            )
            .build()
        )

        self._hub_connection.on("ReceiveSensorData", self.on_sensor_data_received)
        self._hub_connection.on_open(lambda: print("||| Connection opened."))
        self._hub_connection.on_close(lambda: print("||| Connection closed."))
        self._hub_connection.on_error(lambda data: print(
            f"||| An exception was thrown closed: {data.error}"))

    def on_sensor_data_received(self, data):
        try:
            print("Receiving data...")
            print(data[0]["date"] + " --> " + data[0]["data"])
            date = data[0]["date"]
            data = float(data[0]["data"])
            self.send_event_to_database(date, data)
            self.analyze_datapoint(date, data)
        except Exception as err:
            print(err)

    def analyze_datapoint(self, date, data):
        if float(data) >= float(self.t_max):
            self.send_action_to_hvac(date, "TurnOnAc", self.tickets)
        elif float(data) <= float(self.t_min):
            self.send_action_to_hvac(date, "TurnOnHeater", self.tickets)

    def send_action_to_hvac(self, date, action, nb_tick):
        result = requests.get(f"{self.host}/api/hvac/{self.token}/{action}/{nb_tick}")
        details = json.loads(result.text)
        print(details)

    def send_event_to_database(self, timestamp, event):
        table_name = "OxygenCSTemperatureData"
        column_names = ', '.join(["DateCreated", "Temperature"])

        # Removing element after character '+' to convert to datetime object
        timestamp_string_truncated = timestamp.split('+', 1)[0]

        # Slicing last element of string and 
        # converting to datetime object for database insertion
        timestamp_datetime_converted = datetime.strptime(
            timestamp_string_truncated[:-1], '%Y-%m-%dT%H:%M:%S.%f')

        try:
            with DBManager() as database:
                print("Inserting data in database")
                cursor = database.cursor
                sql_query = f'''INSERT INTO {table_name} ({column_names}) VALUES (?, ?)'''
                cursor.execute(sql_query, [timestamp_datetime_converted, event])
                database.commit()
                print("Inserting values in database...")

        except requests.exceptions.RequestException as error:
            print("Exception occurred while attempting to insert data in database. "
            f"Stacktrace: {error}")


if __name__ == "__main__":
    main = Main()
    main.start()
