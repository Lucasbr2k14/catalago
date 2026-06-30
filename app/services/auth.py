from bcrypt import gensalt, hashpw, checkpw

class Auth:
    
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