import psycopg2
import pandas as pd


class PGHelper:
    """A helper to perform basic functions to PostgreSQL DB.

    :param username: PostgreSQL DB user name.
    :param password: PostgreSQL DB password.
    :param dbname: PostgreSQL DB database name.
    """

    def __init__(self, user, password, database):
        self.user = user
        self.password = password
        self.dbname = database
        self.connection = None
        self.connect()

    def execute(self, query, params):
        """Execut query using query and params

        :param query: A PSQL query.
        :param params: A list of parameters for the query.
        """
        if not self.connection:
            self.connect()

        cur = self.connection.cursor()
        cur.execute(query, params)
        self.connection.commit()
        return cur

    def connect(self):
        """Connect to database using proper parameters."""
        self.connection = psycopg2.connect(
            database=self.dbname, user=self.user, password=self.password)
