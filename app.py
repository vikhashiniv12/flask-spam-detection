from flask import Flask, request, jsonify
import json
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

# Load the pre-trained model
model = load_model('spam_detection_model.h5')  # Ensure the model file path is correct

# Load the tokenizer from JSON
with open('token.json') as f:
    tokenizer_json = f.read()  # Read the tokenizer file content
    tokenizer = tokenizer_from_json(json.loads(tokenizer_json))  # Convert JSON string to dictionary

@app.route('/')
def home():
    return "Welcome to the Spam Detection API. Use /predict to classify a message."

@app.route('/predict', methods=['POST'])
def predict():
    # Get the text from the request
    data = request.json
    if 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    message = data['text']

    # Preprocess the text (tokenization, padding, etc.)
    sequence = tokenizer.texts_to_sequences([message])
    padded_sequence = pad_sequences(sequence, maxlen=100)

    # Debugging output
    print(f"Input Message: {message}")
    print(f"Tokenized Sequence: {sequence}")
    print(f"Padded Sequence: {padded_sequence}")

    # Make prediction
    prediction = model.predict(padded_sequence)

    # Debugging output for raw prediction
    print(f"Raw Prediction: {prediction[0][0]}")

    # Adjust prediction threshold if needed
    result = 'Spam' if prediction[0][0] > 0.5 else 'Not Spam'

    return jsonify({'prediction': result})

if __name__ == '__main__':
    # Bind to '0.0.0.0' to allow access from outside the container
    app.run(host='0.0.0.0', port=5000, debug=True)
