import psycopg2
from instance.config import configs
from app.sql import table_create_sql, drop_tables


class DbSetup:
    """Class that creates all tables for the app"""

    def __init__(self, config_name='development'):
        """Create a database connection using a config setting 

        Arguments:
            config_name {[string]}
        """
        connection_string = configs[config_name].CONNECTION_STRING
        self.connection = psycopg2.connect(connection_string)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        """
        Runs the queries to create tables 
        """
        for query in table_create_sql:
            self.cursor.execute(query)

        self.commit()

    def drop(self):
        """
        Drops all tables from the db 
        """
        self.cursor.execute(drop_tables)
        queries = self.cursor.fetchall()

        for i in queries:
            self.cursor.execute(i[0])
        self.commit()

    def commit(self):
        """
        Does the commit actions for the db
        """
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
