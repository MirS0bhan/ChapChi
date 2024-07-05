# myapp/management/commands/initialize_cache.py

from django.core.management.base import BaseCommand
from django.core.cache import cache


from django.conf import settings
from main.views import cache_file_tree



class Command(BaseCommand):
    help = 'Initializes the file tree cache.'

    def handle(self, *args, **options):
        cache_file_tree(settings.UPLOAD_DIR, settings.FILE_TREE_CACHE_KEY)
        self.stdout.write(self.style.SUCCESS('File tree cache initialized successfully!'))