# _sector.py - code by Rye
import warehouse.database.access as dba


class Sector:
    def __init__(self, gid, table):
        self.dba = dba
        self.gid = gid
        self.table = table

    def update_db(self, opt, data):
        """Updates a single field in a database record"""
        con = self.dba.connect('master', 'master')
        con.execute(f"UPDATE {self.table} SET {opt}=:data WHERE id={self.gid}", {'data': data})
        con.commit()

    def retrieve_db(self, opt):
        """Retrieves data from a single field in a database record"""
        con = self.dba.connect('master', 'master')
        cur = con.execute(f"SELECT {opt} FROM {self.table} WHERE id={self.gid}")
        result = cur.fetchone()
        con.commit()
        return result[0] if not None else None

    def new_record(self):
        """Creates a new database record"""
        con = self.dba.connect('master', 'master')
        con.execute(f"INSERT INTO {self.table} (id, stat) VALUES (:id, :stat)", {'id': self.gid, 'stat': 1})
        con.commit()

    def check_db(self):
        """Checks the database for an existing record"""
        result = self.retrieve_db('id')
        if result:
            return False
        else:
            return True