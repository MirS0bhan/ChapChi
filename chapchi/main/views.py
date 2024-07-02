import os

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse, Http404

from .utils import ran_char_num
from .tasks import save_uploaded_file

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
        return render(request, 'main/code.html', {'short_code': code})

    
def download(request, code):
    if len(code) == 5:
        # Directory where uploaded files are stored
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        
        # Search for files starting with the given code
        code = 'X' + code
        for filename in os.listdir(upload_dir):
            if filename.startswith(code):
                file_path = os.path.join(upload_dir, filename)
                return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
        
        # If no file is found
        return render(request, 'main/download.html', {'error_message': 'No file found with the given code.'})
    else:
        return render(request, 'main/download.html', {'error_message': 'Invalid code format.'})
    
    return render(request, 'main/download.html')