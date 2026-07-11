from ...decorators import require_role, login_required
from ...services import ProductService
from ...repository import ProductRepo
from ...database import DataBase
from ...validator import ValidadeJson, Validator

from flask import ( 
    jsonify, 
    g, 
    current_app, 
    request,
    abort
)



from . import api


@api.get('/product/<string:uuid>')
def get_prod(uuid):
    return f"{uuid}", 200


@api.post('/product')
@login_required
@require_role('ADMIN', 'VENDOR')
def create_prod():
    req = request.json
    
    if not req: 
        return abort(400)

    jsonv = ValidadeJson(
        req,
        {'preco', 'quantidade', 'nome'}
    )

    prod_repo = ProductRepo(
        current_app.extensions['db']
    )

    nome = jsonv['nome']
    preco = Validator.price_valid(jsonv['preco'])
    quantidade = Validator.quanti_valid(jsonv['quantidade'])
    user_uuid = g.user_token['uuid']

    prod_ser = ProductService.register(prod_repo, nome, preco, quantidade, user_uuid)

    return jsonify()


# Para pegar produtos
# Será preciso adicionar a quantidade de páginas
@api.get('/products')
@login_required
@require_role('ADMIN', 'VENDOR')
def page_prod():
    """
    Usar parâmetros ?
    /products?page=0&limit=10
    """
    
    page  = request.args.get('page', default=0, type=int)
    limit = request.args.get('limit', default=10, type=int)

    prod_repo = ProductRepo(
        current_app.extensions['db']
    )

    res = ProductService.getPages(
        prod_repo,
        page=page,
        products_quant=limit
    )

    return jsonify(res), 200