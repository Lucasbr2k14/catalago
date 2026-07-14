from psycopg_pool import ConnectionPool
from typing import Any

class DataBase:
    def __init__(self, conn:str):

        self.db_pool = ConnectionPool(
            conninfo = conn,
            min_size = 2,
            max_size = 20
        )

        with open("./app/database/schema.sql", 'r') as file:
            with self.get_pool as pool:
                pool.execute(file.read())


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
    
