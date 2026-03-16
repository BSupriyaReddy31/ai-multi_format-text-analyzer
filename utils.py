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
    """Extracts the most important sentences using LSA Summarization."""
    try:
        if len(text.split()) < 20:
            return text # Don't summarize very short text
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentences_count)
        return " ".join([str(sentence) for sentence in summary])
    except:
        return "Text structure not recognized for summarization."

def get_keywords(text):
    """Identifies the top 5 most frequent meaningful words."""
    words = text.lower().split()
    # Basic list of words to ignore
    stop_words = set(['the', 'and', 'is', 'in', 'it', 'of', 'to', 'for', 'with', 'a', 'this', 'that', 'was', 'on', 'as', 'an'])
    filtered_words = [w for w in words if w.isalpha() and w not in stop_words and len(w) > 2]
    
    most_common = Counter(filtered_words).most_common(5)
    return [word for word, count in most_common]
