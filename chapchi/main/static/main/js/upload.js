const allowedFormats = ['pdf', 'ttf', 'jpeg', 'jpg', 'png'];
const fileUpload = document.getElementById('file-upload');
const fileInfo = document.getElementById('file-info');
const fileName = document.getElementById('file-name');
const fileSize = document.getElementById('file-size');
const filePreview = document.getElementById('file-preview');
const fileIcon = document.getElementById('file-icon');
const form = document.getElementById('upload-form');

const uploadBox = document.getElementById('upload-box');
// ... (rest of the code remains the same)

uploadBox.addEventListener('click', function() {
    fileUpload.click();
});

// ... (rest of the code remains the same)

fileUpload.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const extension = file.name.split('.').pop().toLowerCase();
        if (allowedFormats.includes(extension)) {
            fileName.textContent = file.name;
            fileSize.textContent = (file.size / 1024 / 1024).toFixed(2) + ' MB';
            fileInfo.style.display = 'block';

            // Set file icon based on extension
            fileIcon.className = 'file-icon fas ';
            switch(extension) {
                case 'pdf':
                    fileIcon.className += 'fa-file-pdf';
                    break;
                case 'ttf':
                    fileIcon.className += 'fa-font';
                    break;
                case 'jpeg':
                case 'jpg':
                case 'png':
                    fileIcon.className += 'fa-file-image';
                    break;
            }
            fileIcon.style.display = 'block';

            if (['jpeg', 'jpg', 'png'].includes(extension)) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    filePreview.src = e.target.result;
                    filePreview.style.display = 'block';
                    fileIcon.style.display = 'none';
                }
                reader.readAsDataURL(file);
            } else {
                filePreview.style.display = 'none';
                fileIcon.style.display = 'block';
            }
        } else {
            alert('فرمت فایل مجاز نیست. لطفاً یک فایل با فرمت PDF، TTF، JPEG یا PNG انتخاب کنید.');
            fileUpload.value = '';
            fileInfo.style.display = 'none';
            filePreview.style.display = 'none';
            fileIcon.style.display = 'none';
        }
    }
});

form.addEventListener('submit', function(e) {
    if (!fileUpload.files[0]) {
        e.preventDefault();
        alert('لطفاً یک فایل انتخاب کنید.');
    }
});

// Optional: Add drag and drop functionality
const dropZone = document.querySelector('.card-body');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
    dropZone.classList.add('highlight');
}

function unhighlight(e) {
    dropZone.classList.remove('highlight');
}

dropZone.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    fileUpload.files = files;
    
    // Trigger the change event manually
    const event = new Event('change');
    fileUpload.dispatchEvent(event);
}

