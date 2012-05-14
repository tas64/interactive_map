from server import settings
import psycopg2

class DBWrapper:
    _connection = None

    def _connect_if_need(self):
        if not self._connection:
            conn_string = "host=%s dbname=%s user=%s password=%s" % (settings.OUR_DATABASE_HOST,
                         settings.OUR_DATABASE_NAME, settings.OUR_DATABASE_USER, settings.OUR_DATABASE_PASSWORD)
            self._connection=psycopg2.connect(conn_string)
        #TODO add exceptions handling
        return True

    def _query(self, query):
        self._connect_if_need()
        cursor =  self._connection.cursor()
        cursor.execute(query)
        return cursor

    def fetch_all(self, query):
        cursor = self._query(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def fetch_one(self, query):
        cursor = self._query(query)
        result = cursor.fetchone()
        cursor.close()
        return result

    def execute(self, query):
        cursor = self._query(query)
        self._connection.commit()
        cursor.close()

    def dispose(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    def __del__(self):
        self.dispose()