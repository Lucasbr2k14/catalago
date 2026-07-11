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


        self.postgres_host = getenv("POSTGRES_HOST")
        self.postgres_port = int(getenv("POSTGRES_PORT", 5432))
        self.postgres_user = getenv("POSTGRES_USER")
        self.postgres_pass = getenv("POSTGRES_PASSWORD")
        self.postgres_datb = getenv("POSTGRES_DB_NAME")

        self.dev = str_bool(getenv("DEV"))
