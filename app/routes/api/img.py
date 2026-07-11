from ...decorators import require_role, login_required
from ...services import ImageService

from flask import ( 
    jsonify, 
    g, 
    current_app, 
    request,
    abort,
    send_from_directory
)

from . import api

@api.post('/image')
@login_required
@require_role('VENDOR', 'ADMIN')
def create_image():
    url = ImageService.addImage(request)
    return jsonify({"url": url}), 201


@api.get('/image/<string:file>')
def get_image(file):
    return ImageService.get(file)
