import PyPDF2
from docx import Document
from textblob import TextBlob
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
from collections import Counter
import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract

# 1. Download necessary NLTK resources immediately
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

def extract_text_from_url(url):
    """Fetches text from a webpage."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for s in soup(['script', 'style']): s.extract()
        return soup.get_text(separator=' ')
    except Exception as e:
        return f"Error: {str(e)}"

def extract_text(uploaded_file):
    """Handles multiple file formats including Images."""
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    if file_type == 'pdf':
        reader = PyPDF2.PdfReader(uploaded_file)
        return "".join([p.extract_text() for p in reader.pages])
    elif file_type == 'docx':
        doc = Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs])
    elif file_type in ['png', 'jpg', 'jpeg']:
        return pytesseract.image_to_string(Image.open(uploaded_file))
    elif file_type == 'csv':
        df = pd.read_csv(uploaded_file)
        return f"TABLE_DATA|{df.to_json()}"
    elif file_type == 'xlsx':
        df = pd.read_excel(uploaded_file)
        return f"TABLE_DATA|{df.to_json()}"
    else: # Default for txt
        return str(uploaded_file.read(), "utf-8")

def analyze_text(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    return {
        "word_count": len(text.split()),
        "char_count": len(text),
        "sentiment_score": round(sentiment, 2),
        "sentiment_label": "Positive" if sentiment > 0.1 else "Negative" if sentiment < -0.1 else "Neutral"
    }

def get_summary(text, sentences_count=5):
    """Summarizes the content into distinct key points."""
    try:
        # Clean text: remove extra whitespace to help the parser
        clean_text = " ".join(text.split())
        
        if len(clean_text.split()) < 40:
            return ["Document is too short for a multi-point summary."]

        # Use the PlaintextParser to process the overall text
        parser = PlaintextParser.from_string(clean_text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        
        # LSA (Latent Semantic Analysis) identifies the 'themes' across the whole file
        summary = summarizer(parser.document, sentences_count)
        
        points = [str(sentence).strip() for sentence in summary]
        
        # If the summarizer returns nothing, we manually extract significant sentences
        if not points:
            sentences = [s.strip() for s in clean_text.split('.') if len(s) > 20]
            return sentences[:sentences_count]
            
        return points
    except Exception as e:
        return [f"Analysis interrupted: {str(e)}"]

def get_keywords(text):
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    # Adding extra junk words to filter
    stop_words.update(['which', 'through', 'from', 'also', 'using', 'used', 'would', 'could', 'this', 'that'])
    
    words = text.lower().split()
    filtered_words = [w for w in words if w.isalpha() and w not in stop_words and len(w) > 3]
    
    most_common = Counter(filtered_words).most_common(5)
    return [word for word, count in most_common]
