import os
import aiofiles
import threading
import logging

from datetime import datetime, timedelta

from django.conf import settings
from django.core.cache import cache

from .utils import generate_file_tree, run_in_thread

logger = logging.getLogger(__name__)
UPLOAD_DIR = settings.UPLOAD_DIR

@run_in_thread
async def save_uploaded_file(file_content, file_name, code):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    file_name = f"X{code+file_name}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    logger.info(f"Saving uploaded file {file_name} with {code}")
    async with aiofiles.open(file_path, 'wb') as destination:
        await destination.write(file_content)
    logger.info(f"{code} has saved")

@run_in_thread
def delete_old_files(file_tree=None):
    """
    Delete files that were created more than 5 hours ago.
    """
    now = datetime.now()
    file_tree = file_tree if file_tree != None else tree_file()
    f = filter(lambda file_name: now - datetime.fromtimestamp(os.path.getctime(os.path.join(UPLOAD_DIR, file_name))) > timedelta(hours=5), file_tree.values())
    l = list(map(lambda file_name:os.remove(os.path.join(UPLOAD_DIR, file_name)), f))
    logger.info(f"{len(l)} files had been deleted")
    
@run_in_thread
async def cache_file_tree(directory, cache_key='file_tree', timeout=3600):
    file_tree = generate_file_tree(directory)
    cache.set(cache_key, file_tree, timeout)
    delete_old_files(file_tree)
    logger.info("Refreshing cache")

def tree_file():
    r = cache.get(settings.FILE_TREE_CACHE_KEY)
    if r == None: 
        cache_file_tree(settings.UPLOAD_DIR, settings.FILE_TREE_CACHE_KEY)
    r = cache.get(settings.FILE_TREE_CACHE_KEY)
    return r