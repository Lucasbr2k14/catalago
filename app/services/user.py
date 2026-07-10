from ..models import User
from ..repository import UserRepo
from .segurityService import SegurityService
from ..exceptions import InvalidUser, InternalErr

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
        hash_pass = SegurityService.create_hash_pass(password)
        user_uuid = str(uuid.uuid4())
        return User(name, email, user_name, nascimento, hash_pass, user_uuid)
    
    @staticmethod
    def login(
        user_repo:UserRepo, 
        email:str, 
        password:str, 
    ) -> str:
        
        # Test email
        if not email: 
            raise ValueError("Invalid email")

        test = user_repo.get_user_login(email)

        if not test:
            raise InvalidUser("Invalid email")

        pass_stored, uuid = test

        check_pw:bool = SegurityService.verify_pass(password, pass_stored)
        
        if check_pw == False:
            raise InvalidUser("Invalid password")

        user:User = user_repo.get_user(uuid)
        
        if (not user.uuid or not user.role):
            raise InternalErr()


        token:str = SegurityService.create_jwt(
            user.user_name,
            user.uuid,
            user.role,
        )

        return token
    
    @staticmethod
    def user_redirect(token:str): 
        try:
            SegurityService.validate_jwt(token)
            return True
        except:
            return False