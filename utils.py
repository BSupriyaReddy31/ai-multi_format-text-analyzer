import PyPDF2
from docx import Document
from textblob import TextBlob
import io

def extract_text(uploaded_file):
    """Extracts text based on file extension."""
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    if file_type == 'pdf':
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    
    elif file_type == 'docx':
        doc = Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    
    elif file_type == 'txt':
        return str(uploaded_file.read(), "utf-8")
    
    return None

def analyze_text(text):
    """Performs sentiment and basic stats analysis."""
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity # Ranges from -1 to 1
    
    # Simple word count and stats
    words = text.split()
    results = {
        "word_count": len(words),
        "char_count": len(text),
        "sentiment_score": round(sentiment, 2),
        "sentiment_label": "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
    }
    return results
