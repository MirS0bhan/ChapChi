import os
import aiofiles
from datetime import datetime, timedelta

from django.conf import settings
from django.core.cache import cache

from .utils import generate_file_tree

UPLOAD_DIR = settings.UPLOAD_DIR

async def save_uploaded_file(uploaded_file, code):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    file_name = f"X{code+uploaded_file.name}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    async with aiofiles.open(file_path, 'wb') as destination:
        for chunk in uploaded_file.chunks():
            await destination.write(chunk)

def delete_old_files():
    """
    Delete files that were created more than 5 hours ago.
    """
    now = datetime.now()
    file_tree = cache.get(settings.FILE_TREE_CACHE_KEY)
    f = filter(lambda file_path: now - datetime.fromtimestamp(os.path.getctime(file_path)) > timedelta(hours=5), file_tree.values())
    map(lambda file_path:os.remove(file_path), f)
                
def cache_file_tree(directory, cache_key='file_tree', timeout=3600):
    file_tree = generate_file_tree(directory)
    cache.set(cache_key, file_tree, timeout)
    return file_tree
