import sqlite3
#Credits Mark Otting 
class QuestionModel:
    def __init__(self, database_file):
        self.database_file = database_file

    def run_query(self, sql_query):
        conn = sqlite3.connect(self.database_file)
        c = conn.cursor()
        c.execute(sql_query)
        tables = c.fetchall()
        conn.close()
        return tables

    def get_tables(self):
        sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
        result = self.run_query(sql_query)
        table_list = []
        for table in result:
            table_list.append(table[0])
        return table_list

    def get_columns(self, table):
        sql_query = "PRAGMA table_info({})".format(table)
        result = self.run_query(sql_query)
        table_list = []
        for table in result:
            table_list.append(table[1])
        return table_list

    def get_unconvertable_values(self, table_name, column_name, datatype):
        sql_query = "SELECT id, " + column_name + " FROM " + table_name
        results = self.run_query(sql_query)
        unconvertable_values = []
        for result in results:
            if datatype == "boolean":
                if result[1] != "0" and result[1] != "1":
                    unconvertable_values.append(result)
        return unconvertable_values