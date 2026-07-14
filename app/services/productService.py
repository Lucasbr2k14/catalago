import uuid
from decimal import Decimal
from ..repository import ProductRepo
from ..models import Product
from ..exceptions import ProductExists
from typing import Any
from psycopg.errors import UniqueViolation
from datetime import datetime

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
    def updade(
        r:ProductRepo,
        uuid: str,
        updates:dict
    ):
        
        if 'preco' in updates:
            preco  = Decimal(updates['preco']) * 100
            updates['preco'] = int(preco)

        res = r.update(uuid, updates)
        return res

    @staticmethod
    def __convert_all(tu:tuple):

        name, preco, quantidade, img, uuid_user, create_at = tu

        preco  = Decimal(preco) / 100
        precof = "{:.2f}".format(preco)

        return {
            'name'  : name,
            'preco' : precof,
            'quantidade': quantidade,
            'image_url' : img,
            'create_by' : uuid_user,
            'create_at' : create_at, 
        }


    @staticmethod
    def __convert(tu:tuple) -> dict[str, Any]:
        uuid, nome, preco, quantidade, img_path, create_at, user_name = tu

        preco = Decimal(preco) / 100
        precof = "{:.2f}".format(preco)
        
        return {
            'name': nome,
            'preco': precof,
            'quantidade': quantidade,
            'uuid': uuid,
            'image_path': img_path
        }

