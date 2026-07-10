from bcrypt import gensalt, hashpw, checkpw
from datetime import timezone, datetime, timedelta
from ..exceptions import TokenExpired, TokenInvalid
from flask import current_app
import jwt

class SegurityService:
    
    token_alg = 'HS256'

    @staticmethod
    def create_hash_pass(password:str) -> str:
        salt   = gensalt(rounds=12)
        bpass  = password.encode("utf-8")
        hash_p = hashpw(bpass, salt)
        hash_p = hash_p.decode("utf-8")
        return hash_p 
    
    @staticmethod
    def verify_pass(password:str, stored_pass:str) -> bool:
        return checkpw(
            password.encode("utf-8"),
            stored_pass.encode("utf-8")
        )

    @staticmethod
    def create_jwt(user_name: str, uuid:str, role:str) -> str:
        key = current_app.extensions["configs"].jwt_secret
        exp = current_app.extensions["configs"].jwt_expire

        payload = {
            'user_name': user_name,
            'uuid': uuid,
            'role': role,
            'exp': datetime.now(tz=timezone.utc) + timedelta(seconds=exp)
        }

        return jwt.encode(
            payload=payload,
            key=key, 
            algorithm=SegurityService.token_alg
        )


    @staticmethod
    def validate_jwt(token:str) -> dict:

        key = current_app.extensions["configs"].jwt_secret

        try:
            return jwt.decode(token, key, algorithms=[SegurityService.token_alg])
        except jwt.exceptions.ExpiredSignatureError:
            raise TokenExpired()
        except jwt.exceptions.InvalidSignatureError:
            raise TokenInvalid()
        except jwt.exceptions.DecodeError:
            raise TokenInvalid()
        except jwt.exceptions.InvalidTokenError:
            raise TokenInvalid()