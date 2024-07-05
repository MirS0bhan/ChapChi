import os

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import FileResponse, Http404
from django.core.cache import cache

from .utils import ran_char_num
from .tasks import save_uploaded_file, cache_file_tree, tree_file


def home(request):
    return render(request, 'main/index.html')

@method_decorator(csrf_exempt, name='dispatch')
class FileUploadView(View):
    async def post(self, request):
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        uploaded_file = request.FILES['file']
        code = ran_char_num()
        
        await save_uploaded_file(uploaded_file, code)
        
        # Wait for the task to complete and get the result
        cache_file_tree(settings.UPLOAD_DIR, settings.FILE_TREE_CACHE_KEY)
        return redirect(f'/{code}')

@method_decorator(csrf_exempt, name='dispatch')
class Download(View):
    def get(self, request, code):
        return render(request, 'main/code.html', {'short_code': code})
    
    def post(self, request, code):
        """ Download the file with the given code."""
        
        file_tree = tree_file()
        file_name = file_tree.get(code, None)
        file_path = os.path.join(settings.UPLOAD_DIR, file_name)
        
        if file_path:
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)

            # If no file is found
        return render(request, 'main/download.html', {'error_message': 'No file found with the given code.'})

