from ..database import DataBase
from ..models import Product


class ProductRepo:
    def __init__(self, db:DataBase):
        self.db:DataBase = db


    def __len__(self) -> int:
        return self.items_count()

    def register(self, prod:Product, user_uuid:str):
        query = """
        INSERT INTO produto (
            uuid,
            nome,
            preco,
            quant,
            user_id
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            (SELECT id FROM users WHERE uuid = %s)
        )
        """

        values = (
            prod.uuid,
            prod.nome,
            prod.preco_cents,
            prod.quant,
            user_uuid
        )

        self.db.execute(query, values)

    def update(self): ...
    def delete(self, uuid:str): ...
    def get(self, uuid:str): ...
    def gets(self, limit = 10, offset = 0):
        query = """
        SELECT
            p.uuid,
            p.nome,
            p.preco,
            p.quant,
            u.user_name
        FROM produto AS p
        INNER JOIN "users" AS u
            ON p.user_id = u.id
        LIMIT %s
        OFFSET %s
        """

        return self.db.fetchall(query, (limit, offset))

    def items_count(self) -> int:
        query = "SELECT COUNT(uuid) FROM produto"
        return self.db.fetchone(query)[0]
