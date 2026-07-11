from ...decorators import require_role, login_required
from pathlib import Path

import uuid

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
    upload_dir = current_app.extensions['configs'].upload_dir
    path = Path(upload_dir) / 'images'
    path.mkdir(exist_ok=True, parents=True)
    
    acepted_files = {'jpeg', 'jpg', 'png', 'gif'}

    files = request.files

    if 'image' in files :
        img = files['image']
        extension =  img.filename.split('.')[1]

        if not extension in acepted_files:
            raise ValueError("Invalid file")

        new_name = f"{uuid.uuid4()}.{extension}"

        img.save(path / new_name)

        return jsonify({"url": f"/api/image/{new_name}"}), 201

    return "", 400



@api.get('/image/<string:file>')
def get_image(file):
    upload_dir = current_app.extensions['configs'].upload_dir
    path = Path(upload_dir) / 'images'

    return send_from_directory(
        path.resolve(),
        file
    )
