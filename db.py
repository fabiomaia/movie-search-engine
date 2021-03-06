import psycopg2
from psycopg2.extras import NamedTupleCursor


class PostgresDatabase:
    def __init__(self, name='movie-search-engine', user='fabio'):
        self.name = name
        self.user = user
        self.last_executed_query = ''
        self.results = []

    def query(self, q, args=()):
        self.con = psycopg2.connect(dbname=self.name, user=self.user, cursor_factory=NamedTupleCursor)
        self.cur = self.con.cursor()
        self.last_executed_query = self.cur.mogrify(q, args).decode('utf-8')
        try:
            self.cur.execute(q, args)
            self.con.commit()
            self.results = self.cur.fetchall()
        except psycopg2.ProgrammingError as e:
            print(e)
            self.results = []
        except Exception as e:
            print(e)
            if self.cur:
                self.con.rollback()
        finally:
            if self.cur:
                self.cur.close()
            if self.con:
                self.con.close()
        return self.results

    def close(self):
        if self.cur:
            self.cur.close()
        if self.con:
            self.con.close()
