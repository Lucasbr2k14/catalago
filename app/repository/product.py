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
    
    def gets(
        self,
        limit: int = 10,
        offset: int = 0,
        search: str | None = None
    ):
        query = """
        SELECT
            p.uuid,
            p.nome,
            p.preco,
            p.quant,
            u.user_name
        FROM produto AS p
        INNER JOIN users AS u
            ON p.user_id = u.id
        """

        params = []

        if search:
            query += "\nWHERE p.nome ILIKE %s"
            params.append(f"%{search}%")

        query += """
        ORDER BY p.nome
        LIMIT %s
        OFFSET %s
        """

        params.extend([limit, offset])
        
        return self.db.fetchall(query, tuple(params))

    def items_count(self) -> int:
        query = "SELECT COUNT(uuid) FROM produto"
        return self.db.fetchone(query)[0]
