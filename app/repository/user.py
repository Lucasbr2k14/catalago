from ..models import User
from ..database import DataBase
from psycopg.errors import UniqueViolation
from ..exceptions import *

class UserRepo:
    
    def __init__(self, db:DataBase): 
        self.db = db
    
    def get_user(self, uuid:str): 
        pass

    def get_user_login(self, email:str | None): 
        pass
    
    def update_user(self):
        pass
    
    def register(self, u:User): 
        try:
            query = """
            INSERT INTO 
                users (uuid, name, user_name, email, nascimento, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                u.uuid, 
                u.name, 
                u.user_name, 
                u.email,
                u.nascimento,
                u.password
            )
            self.db.execute(query, values)
        except UniqueViolation:
            raise UserExists()