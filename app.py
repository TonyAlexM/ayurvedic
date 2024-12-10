from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load your trained model
model = load_model('leaf_model.h5')

# Species to uses mapping
species_uses = {
    0: {"name": "Brahmi", "uses": "Enhance memory, anxiety."},
    1: {"name": "Tulsi", "uses": "Indigestion, heart diseases, respiratory diseases."},
    2: {"name": "Neem", "uses": "Leprosy, eye disorders, bloody nose."},
}

def prepare_image(image):
    image = image.resize((224, 224))  # Resize image to match model input
    image_array = np.array(image) / 255.0  # Normalize the image
    return np.expand_dims(image_array, axis=0)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    try:
        image = Image.open(file)
        prepared_image = prepare_image(image)
        prediction = model.predict(prepared_image)
        species_idx = np.argmax(prediction)
        
        species_info = species_uses.get(species_idx, {"name": "Unknown", "uses": "Information not available."})
        return jsonify({'species': species_info['name'], 'uses': species_info['uses']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

