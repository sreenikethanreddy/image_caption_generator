from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from PIL import Image
import io
import nltk
import os
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Download NLTK tokenizer (if not already present)
nltk.download('punkt')

# Load BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
model.eval()

@app.route('/')
def index():
    return render_template('index.html')  # Assumes you have 'templates/index.html'

@app.route('/upload', methods=['POST'])
def upload_image():
    print("📥 Received image upload", flush=True)

    if 'image' not in request.files:
        print("❌ No image part in request", flush=True)
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    if file.filename == '':
        print("❌ No image selected", flush=True)
        return jsonify({'error': 'No image selected'}), 400

    try:
        # Read and convert image
        image = Image.open(file.stream).convert('RGB')
        print("✅ Image opened and converted", flush=True)

        # Process image for captioning
        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            outputs = model.generate(**inputs)
        caption = processor.decode(outputs[0], skip_special_tokens=True)

        # Optional: clean up caption
        tokens = nltk.word_tokenize(caption)
        caption = ' '.join(tokens)

        print("✅ Caption generated:", caption, flush=True)
        return jsonify({'caption': caption})
    except Exception as e:
        import traceback
        print("❌ Exception occurred:", flush=True)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
