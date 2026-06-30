from ..models import User
from .auth import Auth
import uuid


class UserService:

    @staticmethod
    def register(
        name: str,
        email:str,
        user_name: str,
        nascimento: str,
        password: str,
    ):
        hash_pass = Auth.create_hash_pass(password)
        user_uuid = str(uuid.uuid4())
        return User(name, email, user_name, nascimento, hash_pass, user_uuid)