document.getElementById('imageInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.getElementById('previewImg');
            img.src = e.target.result;
            document.getElementById('imagePreview').classList.remove('hidden');
            document.getElementById('generateCaption').classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('generateCaption').addEventListener('click', function() {
    const input = document.getElementById('imageInput');
    const file = input.files[0];
    if (!file) {
        alert('Please select an image');
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('captionOutput').innerText = 'Error: ' + data.error;
        } else {
            document.getElementById('captionOutput').innerText = 'Caption: ' + data.caption;
        }
    })
    .catch(error => {
        document.getElementById('captionOutput').innerText = 'Error: ' + error.message;
    });
});