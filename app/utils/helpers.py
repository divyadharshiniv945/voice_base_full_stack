import os
import secrets
from werkzeug.utils import secure_filename
from config import Config


def allowed_file(filename: str) -> bool:
    if not filename:
        return False
    ext = filename.rsplit('.', 1)[-1].lower()
    return ext in Config.ALLOWED_IMAGE_EXTENSIONS


def save_profile_image(image_file):
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        random_hex = secrets.token_hex(8)
        _, extension = os.path.splitext(filename)
        image_name = f'user_{random_hex}{extension}'
        upload_path = os.path.join(Config.UPLOAD_FOLDER, image_name)

        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        image_file.save(upload_path)
        return image_name
    return None
