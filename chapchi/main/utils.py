import os
import logging
from random import choices
from string import ascii_lowercase, digits

t = ascii_lowercase + digits * 6 # balance between lowercase and digits; ascii:28, digits:10
logger = logging.getLogger(__name__)

def ran_char_num():
    return ''.join(choices(t,k=5))

def generate_file_tree(directory):
    logger.info("generating file tree")
    file_tree = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith('X') and len(file) > 5:
                code = file[1:6]  # Extract the 5-digit code
                file_tree[code] = file
    return file_tree

import threading
import asyncio
from functools import wraps

def run_in_thread(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            # If it's an async function, run it in a new event loop in a separate thread
            def run_async():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(func(*args, **kwargs))
                loop.close()
            thread = threading.Thread(target=run_async)
        else:
            # If it's a regular function, run it directly in a separate thread
            thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        
        thread.start()
        return thread
    return wrapper