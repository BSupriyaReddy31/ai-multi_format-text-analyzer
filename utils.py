import PyPDF2
from docx import Document
from textblob import TextBlob
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
from collections import Counter

# Ensure necessary data is downloaded
nltk.download('punkt')

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
    sentiment = blob.sentiment.polarity
    words = text.split()
    results = {
        "word_count": len(words),
        "char_count": len(text),
        "sentiment_score": round(sentiment, 2),
        "sentiment_label": "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
    }
    return results

def get_summary(text, sentences_count=3):
    """Improved summary logic."""
    try:
        # If text is too short, just return the text itself
        if len(text.split()) < 50:
            return text 
            
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentences_count)
        
        # If summarizer fails to pick sentences, fall back to first few
        if not summary:
            return " ".join(text.split()[:50]) + "..."
            
        return " ".join([str(sentence) for sentence in summary])
    except Exception as e:
        return f"Could not summarize: {str(e)}"

def get_keywords(text):
    """Uses a more robust stop-word filter."""
    import nltk
    from nltk.corpus import stopwords
    nltk.download('stopwords')
    
    stop_words = set(stopwords.words('english'))
    # Add custom words that you keep seeing but don't want
    custom_stops = {'which', 'through', 'from', 'also', 'using', 'used', 'would'}
    stop_words.update(custom_stops)
    
    words = text.lower().split()
    # Only keep words that are alphabetic, not in stop_words, and longer than 3 chars
    filtered_words = [w for w in words if w.isalpha() and w not in stop_words and len(w) > 3]
    
    most_common = Counter(filtered_words).most_common(5)
    return [word for word, count in most_common]
