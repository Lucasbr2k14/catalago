from psycopg_pool import ConnectionPool
from os import getenv
from typing import Any

class DataBase:
    def __init__(self):
        self.host = getenv("POSTGRESS_HOST")
        self.port = int(getenv("POSTGRESS_PORT", 5432))
        self.user = getenv("POSTGRESS_USER")
        self.password = getenv("POSTGRESS_PASSWORD")
        self.dbname = getenv("POSTGRESS_DB_NAME")
    
        self.db_pool = ConnectionPool(
            conninfo = self._get_connect(),
            min_size = 2,
            max_size = 20
        )


    def _get_connect(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{str(self.port)}/{self.dbname}"


    @property
    def get_pool(self):
        return self.db_pool.connection()


    def execute(self, sql:str, parms:tuple = ()):
        with self.get_pool as pool:
            with pool.cursor() as cur:
                cur.execute(sql, parms)
            pool.commit()
    

    def fetchall(self, sql:str, params:tuple = ()) -> list[tuple]:
        with self.get_pool as pool:
            with pool.cursor() as cur:
                cur.execute(sql, params)
                return cur.fetchall()


    def fetchone(self, sql:str, parms:tuple = ()) -> Any:
        with self.get_pool as pool:
            with pool.cursor() as cur:
                cur.execute(sql, parms)
                return cur.fetchone()
    
