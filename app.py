from flask import Flask, render_template, request, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import nltk
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_url_path='/static')
# Download NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Load model
try:
    logger.info("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained("./model")
    model = AutoModelForSequenceClassification.from_pretrained("./model")
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Model loading error: {str(e)}")
    raise

# Intent labels
INTENT_LABELS = {
    0: 'Play Music',
    1: 'Add to Playlist',
    2: 'Rate Book',
    3: 'Search Event',
    4: 'Book Restaurant',
    5: 'Get Weather',
    6: 'Search Creative Work'
}

@app.route('/')
def home():
    logger.debug("Home page requested")
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        text = request.form.get('text', '')
        logger.debug(f"Received text: {text}")
        
        if not text:
            logger.warning("Empty request received")
            return jsonify({'error': 'Please enter text'}), 400
        
        # Preprocess text
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', '', text)
        
        # Classify text
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding='max_length')
        outputs = model(**inputs)
        predicted = torch.argmax(outputs.logits).item()
        
        result = {
            'text': text,
            'intent': INTENT_LABELS.get(predicted, 'Unknown'),
            'confidence': float(torch.max(torch.softmax(outputs.logits, dim=1)))
        }
        
        logger.debug(f"Prediction result: {result}")
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Processing error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)