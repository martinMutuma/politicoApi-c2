"""app/v2/model/__init__.py"""
import os
import re
import psycopg2

from app.db_setup import DbSetup
config = os.getenv('FLASK_ENV', 'development')
db = DbSetup(config)


class BaseModel(object):
    """Base model to host querry builders for the rest of the models
    """
    connection = db.get_connection()
    cursor = db.get_cursor()
    table_name = None
    primary_key = 'id'
    order_by = primary_key
    fields = []
    errors = []
    sub_set_cols = [primary_key]
    id = None

    def __init__(self):
        """ Model instance
        Arguments: table {[string]} -- [name of the table]
        """
        self.select_query = """SELECT * FROM {}""".format(self.table_name)
        self.where_clause = ''
        self.compiled_select = ""
        self.column_names = []
        self.clean_insert_dict()

    def select(self, fields=[]):
        """Builds the select part of the query
        Keyword Arguments:
            fields {str} -- [fields to select] (default: {"*"})
            fields {List} -- [fields to select])
        """
        if len(fields) > 0:
            formated_fields = ",".join(fields)
            self.select_query = """SELECT {} FROM {}""".format(
                formated_fields, self.table_name)
        else:
            self.select_query = """SELECT * FROM {}""".format(self.table_name)
        return self

    def insert(self, new_data_dict):
        """Compiles the insert statement
        Arguments: new_data_dict {dicti} -- {fieldname:value, fieldname:value}
        """
        print(new_data_dict)
        if len(new_data_dict) == 0:
            return False
        columns = ",".join(new_data_dict.keys())
        formated = []
        for x in new_data_dict.values():
            val = "'{}'".format(x)
            formated.append(val)
        set_values = ",".join(formated)
        query = "INSERT INTO {} ({}) VALUES({}) RETURNING {};".format(
            self.table_name, columns, set_values, ','.join(self.sub_set_cols))

        self.execute_query(query, True)
        try:
            result = self.cursor.fetchone()
            if result:
                self.id = result[self.primary_key]
                self.add_result_to_self(result)
        except psycopg2.ProgrammingError as errorx:
            result = None
            print(errorx)

    def update(self, data_update_dict, pry_key):
        """Compiles the Update querr
        Arguments: data_update_dict {[type]} -- [description]
        """
        set_part = ''
        count = 0
        data_len = len(data_update_dict)
        for key, value in data_update_dict.items():
            count += 1
            if count == data_len:
                set_part += " {}='{}'".format(key, value)
            else:
                set_part += " {}='{}',".format(key, value)
        self.where({self.primary_key: pry_key})
        query = "UPDATE {} SET {} ".format(self.table_name, set_part)
        query += self.where_clause
        query += " RETURNING {}".format(','.join(self.sub_set_cols))
        self.execute_query(query, True)
        try:
            result = self.cursor.fetchone()
            if result:
                self.id = result[self.primary_key]
                self.add_result_to_self(result)
        except psycopg2.ProgrammingError as errorx:
            result = None
            print(errorx)
        self.where_clause = ''
        return result

    def where(self, where_dict, operator="AND"):
        """sets the where clause for select,delete and update queries
            Arguments:whereDict {[dict()]} -- [fieldname:value,
             fieldname !=: value,
             fieldname >=: value ]
        """
        special_chars = r'[><=!]'
        clause = ""
        if "WHERE" not in self.where_clause:
            clause = "WHERE "
        count = 0
        if bool(re.search(special_chars, self.where_clause)) is True:
            count = 2
        for key, value in where_dict.items():
            count += 1
            comparison = '='
            if bool(re.search(special_chars, key)) is True:
                comparison = ''
            if count == 1:
                clause += " {}{}'{}'".format(key, comparison, value)
            else:
                clause += " {} {}{}'{}'". format(operator,
                                                 key, comparison, value)
        self.where_clause += clause
        return self

    def get(self, single=True,  number="all",):
        """Builds and executes the select querry
        """
        query = self.compile_select()
        self.execute_query(query)
        self.where_clause = ''
        if single is True:
            try:
                result = self.cursor.fetchone()
                if result is not None:
                    self.id = result[self.primary_key]
                    self.add_result_to_self(result)
            except psycopg2.ProgrammingError as errorx:
                result = None
                print(errorx)
        elif type(number) == int:
            result = self.cursor.fetchmany(number)
        else:
            result = self.cursor.fetchall()
        return result

    def get_one(self, id):
        """Creates self variables with data from db  """
        self.where({self.primary_key: id})
        query = self.compile_select()
        self.execute_query(query)
        self.where_clause = ''
        try:
            result = self.cursor.fetchone()
            if result:
                self.id = result[self.primary_key]
                self.add_result_to_self(result)
        except psycopg2.ProgrammingError as errorx:
            result = None
            print(errorx)
        return result

    def compile_select(self):
        """compiles the select querry
        """
        if self.select_query:
            query = self.select_query
        else:
            query = self.select()
        if self.where_clause != '' and "WHERE" in self.where_clause:
            query += ' ' + self.where_clause
        self.compiled_select = query

        return self.compiled_select

    def execute_query(self, query, commit=False):
        """To central place to do query execution
        Arguments: query {[str]} -- [compild query]
        """
        try:
            self.cursor.execute(query)
            if config != 'production':
                print("========execute query=====")
                print(self.cursor.statusmessage)
                print(query)
                print("========execute query end=====")
            if commit is True:
                self.connection.commit()
            self.where_clause = ''
        except psycopg2.Error as errorx:
            if config != 'production':
                print(errorx)
            self.errors.append("Error executing `{}`".format(query))
            return False

    def clean_insert_dict(self, dynamic_dict={}, full=True):
        """cleans a dictionaly according using table column names
        Keyword Arguments:
            dynamic_dict {dict} -- [description] (default: {{}})
        Returns: [dict] -- [with insertable colums]
        """
        query = "SELECT * FROM {} limit 1".format(self.table_name)
        self.execute_query(query)

        if self.cursor.description is not None:
            self.column_names = [row[0]for row in self.cursor.description]
        clean_dict = {}
        if len(self.column_names) == 0:
            return dynamic_dict
        if full is True:
            for col in self.column_names:
                clean_dict[col] = dynamic_dict.get(col, None)
        else:
            for key, value in dynamic_dict.items():
                key_l = key.lower()
                if key_l in self.column_names:
                    clean_dict[key] = value
        return clean_dict

    def sub_set(self, list_to_get=None):
        """gets a dictinary with the fields in the list_to_get
        Keyword Arguments:
            list_to_get {list} -- [description] (default: {[]})
        Returns: [dict] -- [subset of self]
        """
        if list_to_get is None:
            list_to_get = self.sub_set_cols
        list_to_get = [x.lower() for x in list_to_get]

        sub_set = dict.fromkeys(list_to_get, None)
        for key, value in self.__dict__.items():
            if key in list_to_get:
                sub_set[key] = value
        return sub_set

    def delete(self, id=None):
        """Deletes an item from the db

        Arguments:
            id {[type]} -- [description]
        """
        if id is None and self.where_clause == '':
            return False
        self.where({self.primary_key: id})
        query = "DELETE FROM {} ".format(self.table_name)
        query += self.where_clause
        self.execute_query(query, True)

    def check_exist(self):
        """Check if a record exists
        Returns:
            [type] -- [description]
        """
        if self.where_clause != '' and self.get() is None:
            status = False
        else:
            status = True

        return status

    def add_result_to_self(self, result={}):
        """Adds a dictionary to self as a valiable
        Keyword Arguments:
            result {dict} -- [description] (default: {{}})
        """
        self.__dict__.update(result)
