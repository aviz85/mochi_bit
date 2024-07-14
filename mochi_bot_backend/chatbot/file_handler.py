import os
from werkzeug.utils import secure_filename
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    if file and allowed_file(file.name):
        filename = secure_filename(file.name)
        path = default_storage.save(f'uploads/{filename}', ContentFile(file.read()))
        return path
    return None

def delete_file(file_path):
    if default_storage.exists(file_path):
        default_storage.delete(file_path)
        return True
    return False

def get_file_url(file_path):
    return default_storage.url(file_path)