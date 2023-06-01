import pyodbc
import json


class DatabaseUtility:

    COURSE_RECORD_TABLE_NAME = 'CourseRecord'

    def __init__(self, filename):
        self.__config = None
        with open(filename) as f:
            self.__config = json.load(f)

        # Connect to the database
        server = f'{self.__config["server name"]}.database.windows.net'
        database = self.__config['database']
        username = self.__config['username']
        password = input("Enter database password: ")
        driver = '{ODBC Driver 18 for SQL Server}'
        self.__cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

        # Create a cursor object
        self.__cursor = self.__cnxn.cursor()

    def select_data(self, table_name):
        """
        For each schema in the database, select all the records from the table named passed in
        :return: a pandas dataframe of all the records
        """
        # Get all the schemas in the database
        schemas = self.__cursor.execute("SELECT schema_name FROM information_schema.schemata").fetchall()

        records = []
        for schema in schemas:
            records.extend(self.select_all_from_table(f"{schema.schema_name}.{table_name}"))

        return records

    def select_all_from_table(self, table_name):
        """
        Select all records from a table and return it as a pandas dataframe
        :param table_name: string of the table name
        :return: a pandas dataframe of the table
        """
        query_str = f'SELECT * FROM {table_name}'
        return self.__cursor.execute(query_str).fetchall()

    def create_course_record_table(self):
        # Create the table
        self.__cursor.execute('''
            CREATE TABLE {} (
                term_id INT NOT NULL,
                course_id INT NOT NULL,
                user_id INT NOT NULL
            )
        '''.format(self.COURSE_RECORD_TABLE_NAME))

        # Commit the transaction
        self.__cnxn.commit()

    def insert_course_record(self, term_id, course_id, user_id):
        self.__cursor.execute(f'INSERT INTO {self.COURSE_RECORD_TABLE_NAME} (term_id, course_id, user_id)'
                              f'VALUES ({term_id}, {course_id}, {user_id})')
        self.__cursor.commit()

    def select_course_record(self):
        query_str = f'SELECT * FROM {self.COURSE_RECORD_TABLE_NAME} '
        self.__cursor.execute(query_str)
        for row in self.__cursor:
            term_id = row.term_id
            course_id = row.course_id
            user_id = row.user_id
            print(f'Term ID: {term_id}, Course ID: {course_id}, User ID: {user_id}')
    def create_schema(self, schema_name):
        self.__cursor.execute(f'CREATE SCHEMA {schema_name}')
        self.__cnxn.commit()
    def close_connection(self):
        # Close the connection
        self.__cnxn.close()
