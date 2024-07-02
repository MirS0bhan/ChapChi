import os
from celery import shared_task
import aiofiles
from django.conf import settings
from .utils import ran_char_num

@shared_task
async def save_uploaded_file(file_content, original_filename):
    upload_folder = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    
    code = ran_char_num()
    file_name = f"X{code+original_filename}"
    file_path = os.path.join(upload_folder, file_name)
    
    async with aiofiles.open(file_path, 'wb') as destination:
        await destination.write(file_content)
    
    return code