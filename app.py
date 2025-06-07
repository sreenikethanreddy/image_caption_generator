from flask import Flask, request, jsonify, render_template
from PIL import Image
import io
import nltk
from transformers import BlipProcessor, BlipForConditionalGeneration
import os

app = Flask(__name__)

# Download NLTK data
nltk.download('punkt')

# Load BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    try:
        # Open and process image
        image = Image.open(file.stream).convert('RGB')
        
        # Generate caption using BLIP
        inputs = processor(images=image, return_tensors="pt")
        outputs = model.generate(**inputs)
        caption = processor.decode(outputs[0], skip_special_tokens=True)
        
        # Tokenize caption for consistency with document
        tokens = nltk.word_tokenize(caption)
        caption = ' '.join(tokens)
        
        return jsonify({'caption': caption})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)