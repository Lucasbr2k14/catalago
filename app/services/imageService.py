from pathlib import Path
from PIL import Image, ImageOps
from uuid import uuid4

from flask import current_app, send_from_directory

def process_image(file, upload_dir:Path):
    """
    Processa uma imagem enviada pelo o usuário.
    - Converte para webp
    - Reduz qualidade
    - Reduz resolução
    - Converte para RGB
    """
    upload_dir.mkdir(exist_ok=True, parents=True)

    filename = f"{uuid4()}.webp"
    filepath = upload_dir / filename 

    img = Image.open(file)
    img = ImageOps.exif_transpose(img)

    img = img.convert("RGB")
    img.thumbnail((800,800))

    img.save(
        filepath,
        format="WEBP",
        quality=80,
        optimize=True,
        method=6
    )

    return filename


class ImageService:
    
    @staticmethod
    def addImage(request)-> str:
        upload_dir = current_app.extensions['configs'].upload_dir
        path = Path(upload_dir) / 'images'
        
        if not 'image' in request.files:
            raise ValueError("Invalid file")
        
        try:    
            name = process_image(
                request.files['image'],
                path
            )
        except Exception as e:
            raise ValueError("Invalid file")

        return f"/api/image/{name}"


    @staticmethod
    def get(file):
        upload_dir = current_app.extensions['configs'].upload_dir
        path = Path(upload_dir) / 'images'

        return send_from_directory(
            path.resolve(),
            file
        )