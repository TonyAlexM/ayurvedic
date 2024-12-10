import streamlit as st
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
import os

# Load pre-trained models
model_path = "path/to/your/model.h5"
leaf_model = load_model(model_path)

# List of Ayurvedic leaves with their details
ayurvedic_leaves = {
    0: {"name": "Neem", "scientific_name": "Azadirachta indica", "benefits": "Antimicrobial, anti-inflammatory"},
    1: {"name": "Turmeric", "scientific_name": "Curcuma longa", "benefits": "Anti-inflammatory, antioxidant"},
    # Add more leaves here...
}

def predict_leaf(image):
    img = tf.io.read_file(image)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, (224, 224))
    img = tf.cast(img, tf.float32) / 255.0
    img = tf.expand_dims(img, axis=0)
    
    prediction = leaf_model.predict(img)
    return tf.argmax(prediction, axis=-1).numpy()[0]

def main():
    st.title("Ayurvedic Leaf Identification")

    uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        st.image(image, caption="Uploaded Image", width=300)
        
        result = predict_leaf(uploaded_file.name)
        
        st.write(f"Predicted leaf: **{ayurvedic_leaves[result]['name']}**")
        st.write(f"Scientific name: **{ayurvedic_leaves[result]['scientific_name']}**")
        st.write(f"Benefits: **{ayurvedic_leaves[result]['benefits']}**")

if __name__ == "__main__":
    main()
