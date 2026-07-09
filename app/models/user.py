from datetime import datetime


class User:
    def __init__(
        self,
        name: str,
        email:str,
        user_name: str,
        nascimento: str,
        password: str | None = None,
        uuid: str | None = None,
        role: str | None = None
    ):
        self.name:str = name
        self.email:str = email
        self.user_name:str = user_name
        self.nascimento:datetime = self.__date(nascimento)
        self.password:str | None = password
        self.uuid: str | None = uuid
        self.role: str | None = role
    
    @staticmethod
    def __date(date:str | datetime) -> datetime:
        
        if isinstance(date, datetime):
            return date
        if isinstance(date, str):
            return datetime.fromisoformat(date)