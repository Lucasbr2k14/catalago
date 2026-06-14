from os import getenv


class db:
    def __init__(self):
        self.host = getenv("POSTGRESS_HOST")
        self.port = int(getenv("POSTGRESS_PORT", 532))
        self.user = getenv("POSTGRESS_USER")
        self.password = getenv("POSTGRESS_PASSWORD")
        self.dbname = getenv("POSTGRESS_DB_NAME")
    
    

