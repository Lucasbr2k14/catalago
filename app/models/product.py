import uuid
from decimal import Decimal

class Product:
    def __init__(
        self,
        nome:str,
        preco: Decimal,
        quant:int,
        uuid:str | None,
    ):
        self.nome:str = nome
        self.quant:int = quant
        self.uuid:str | None = uuid 
        self.preco:Decimal = preco

    @property
    def preco_cents(self):
        return int(self.preco * 100)
    