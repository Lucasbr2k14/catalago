from datetime import datetime


class User:
    def __init__(
        self,
        name: str,
        email:str,
        user_name: str,
        nascimento: str,
        password: str,
        uuid: str | None = None
    ):
        self.name:str = name
        self.email:str = email
        self.user_name:str = user_name
        self.nascimento:datetime = datetime.fromisoformat(nascimento)
        self.password:str = password
        self.uuid: str | None = uuid
    