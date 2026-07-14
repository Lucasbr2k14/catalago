from os import getenv

def str_bool(string):
    if string == "True":
        return True
    elif string == "False":
        return False


class Configs:
    def __init__(self):
        self.jwt_secret = getenv("JWT_TOKEN", "")
        self.jwt_expire = int(getenv("JWT_EXPIRATION_S", 3600))
        self.upload_dir = getenv("UPLOAD", "./uploads/")


        self.postgres_conn = getenv("POSTGRES_CONN") # Aqui é a conexão

        self.dev = str_bool(getenv("DEV"))

        self.host = getenv("HOST")
        self.port = int(getenv("PORT", 8080))