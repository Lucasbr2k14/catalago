from ..models import User
from ..database import DataBase
from psycopg.errors import UniqueViolation
from ..exceptions import *

class UserRepo:
    
    def __init__(self, db:DataBase): 
        self.db = db
    
    def get_user(self, uuid:str) -> User:
        query = """
        SELECT 
            u.uuid, u.name, u.user_name, u.email, u.nascimento, u.create_at, r.nome
        FROM "users" AS u
        INNER JOIN user_roules AS r
            ON u.role_id = r.id
        WHERE
            u.uuid = %s
        """

        uuid2, name, user_name, email, nascimento, create_at, role = self.db.fetchone(query, (uuid,))

        return User(
            name=name,
            email=email,
            user_name=user_name,
            nascimento=nascimento,
            uuid=uuid2,
            role=role
        )


    def get_user_login(self, email:str | None) -> tuple[str, str]: 
        query = """
        SELECT password, uuid FROM users WHERE email = %s
        """
        res = self.db.fetchone(query, (email,))
        
        return res

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