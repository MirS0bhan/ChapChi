import os
import aiofiles
from datetime import datetime, timedelta

from django.conf import settings


async def save_uploaded_file(uploaded_file, code):
    upload_folder = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    
    file_name = f"X{code+uploaded_file.name}"
    file_path = os.path.join(upload_folder, file_name)
    
    async with aiofiles.open(file_path, 'wb') as destination:
        for chunk in uploaded_file.chunks():
            await destination.write(chunk)

def delete_old_files():
    """
    Delete files that were created more than 5 hours ago.
    """
    now = datetime.now()
    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        for file in files:
            file_path = os.path.join(root, file)
            created_at = os.path.getctime(file_path)
            if (now - datetime.fromtimestamp(created_at)) > timedelta(hours=5):
                os.remove(file_path)