import uuid
from decimal import Decimal
from ..repository import ProductRepo
from ..models import Product
from ..exceptions import ProductExists
from typing import Any
from psycopg.errors import UniqueViolation


class ProductService:
    
    @staticmethod
    def register(
        repository: ProductRepo, 
        nome:  str,
        preco: Decimal, 
        quant: int,
        image_url:str,
        u_uuid:str
    ):
        if not nome or not preco or not quant:
            raise ValueError()

        p_uuid = str(uuid.uuid4())

        product = Product(nome, preco, quant, image_url, p_uuid)
        
        try:
            repository.register(product, u_uuid)
        except UniqueViolation:
            raise ProductExists()


    @staticmethod
    def getPages(
        r: ProductRepo,
        search:str | None = None,
        page:int = 0,
        products_quant:int = 10
    ):
        total = len(r)
        pages = total // products_quant + 1

        c = ProductService.__convert
        prods = r.gets(
            limit  = products_quant,
            offset = products_quant * page,
            search = search
        )

        prod = [ c(p) for p in prods ]
        
        return {
            'products': prod,
            'total pages': pages,
            'page': page,
            'total': total,
        }


    @staticmethod
    def get(
        r:ProductRepo,
        uuid:str,
    ):
        res = r.get(uuid)
        prod = ProductService.__convert_all(res)
        return prod


    @staticmethod
    def __convert_all(tu:tuple):
        preco  = Decimal(tu[1]) / 100
        precof = "{:.2f}".format(preco)

        return {
            'name': tu[0],
            'preco': precof,
            'quantidade': tu[2],
            'image_url': tu[3],
            'create_by': tu[4],
            'create_at': tu[5],
        }


    @staticmethod
    def __convert(tu:tuple[str, str, int, int, str]) -> dict[str, Any]:
        preco = Decimal(tu[2]) / 100
        precof = "{:.2f}".format(preco)
        
        return {
            'name': tu[1],
            'preco': precof,
            'quantidade': tu[3],
            'uuid': tu[0]
        }
    