from datetime import datetime
from decimal import Decimal
from typing import Any

class Validator:
    @staticmethod
    def register_user(
        name:str,
        user_name:str,
        email:str,
        password:str,
        nascimento:str
    ):
        
        errs = []

        if not name:
            errs.append("name")
        if not user_name:
            errs.append("user name")
        if not Validator.test_email(email):
            errs.append("email")
        if not Validator.test_password(password):
            errs.append("Password")
        if not Validator.test_date(nascimento):
            errs.append("nascimento")

        if errs:
            raise ValueError(f"Invalid filds {", ".join(errs)}" )

    @staticmethod
    def test_email(email:str) -> bool:
        if not email:
            return False
        if not "@" in email:
            return False
        if not "." in email:
            return False
        
        return True
    
    @staticmethod
    def test_password(password:str) -> bool:
        if len(password) < 4:
            return False
        
        return True

    @staticmethod
    def test_date(date:str, format="%Y-%m-%d") -> bool:
        
        try:
            datetime.strptime(date, format)
            return True
        except ValueError:
            return False


    @staticmethod
    def price_valid(price:str) -> Decimal:
        return Decimal(price)


    @staticmethod
    def quanti_valid(quant:int) -> int:
        if quant >= 0:
            return quant
        else:
            raise ValueError("Quantidade is invalid.")


class ValidateForm:

    form_type = "application/x-www-form-urlencoded"

    def __init__(self, form, filds:set[str]):
        self.filds_set = filds
        self.form = form

        if self.__validade():
            raise ValueError("Invalid form")

    def __validade(self):
        keys = set(list(self.form.keys()))
        return self.filds_set - keys
    
    def get(self, name):
        return self.form[name]
    
    def __getitem__(self, key):
        return self.get(key)



class ValidadeJson:
    def __init__(self, json_dict:dict[str, Any], filds:set[str]):
        self.filds_set = filds
        self.json_dict = json_dict

        if self.__validate():
            raise ValueError("Invalid json")

    def __validate(self):
        keys = set(self.json_dict.keys())
        return self.filds_set - keys

    def get(self, name):
        return self.json_dict[name]

    def __getitem__(self, key):
        return self.get(key)