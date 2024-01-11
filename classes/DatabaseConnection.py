import sqlite3


# Create a cursor to a SQL database. Using connection.execute instead of cursor.execute() would be a 'non-standard shortcut'.
# cursor = sqlite3.connect('database.db').cursor()
class DatabaseConnection:
    def __init__(self, database='database.db'):
        self.database = database

    def connect(self):
        return sqlite3.connect(self.database)
