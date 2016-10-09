import os
import magic
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError

def validate_file_type(upload):
    #get MIME type.
    upload.seek(0)
    file_type = magic.from_buffer(upload.file.read(1024), mime = True)
    if file_type not in settings.FILE_TYPES:
        raise ValidationError('File format not supported:{0}'.format(file_type))
