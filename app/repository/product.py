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
            img_path,
            user_id
        )
        VALUES (
            %s,
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
            prod.image_url,
            user_uuid
        )

        self.db.execute(query, values)


    def update(self, uuid: str, update: dict):
        campos = []
        valores = []

        if "preco" in update:
            campos.append("preco = %s")
            valores.append(update["preco"])

        if "quantidade" in update:
            campos.append("quant = %s")
            valores.append(update["quantidade"])

        if "image_url" in update:
            campos.append("img_path = %s")
            valores.append(update["image_url"])

        if not campos:
            return

        valores.append(uuid)

        query = f"""
        UPDATE produto
        SET {', '.join(campos)}
        WHERE uuid = %s
        """

        self.db.execute(query, tuple(valores))
        return True

    def delete(self, uuid:str): ...


    def get(self, uuid:str):
        """
        Função retorna uma tupla, com as infomações do produto
        na seguinte ordem:
        0 - nome
        1 - preço em centavos
        2 - quantidade
        3 - imagem url
        4 - uuid do usuário
        5 - create at
        """
        query = """
        SELECT
            p.nome,
            p.preco,
            p.quant,
            p.img_path,
            u.uuid,
            p.create_at
        FROM produto AS p
        INNER JOIN users AS u
            ON p.user_id = u.id
        WHERE 
            p.uuid = %s
        """
        
        res = self.db.fetchone(query, (uuid,));

        return res
    
    def gets(
        self,
        limit: int = 10,
        offset: int = 0,
        search: str | None = None
    ):
        """
        Função gets pega os produtos da segunte forma tupla de tupla,
        na ordem
        0 - uuid
        1 - nome
        2 - preço
        3 - quantidade
        4 - caminho para a imagem
        5 - quando criado
        6 - nome de usuário
        """
        
        query = """
        SELECT
            p.uuid,
            p.nome,
            p.preco,
            p.quant,
            p.img_path,
            p.create_at,
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
