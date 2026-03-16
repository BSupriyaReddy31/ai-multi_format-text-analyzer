import streamlit as st
from utils import extract_text, analyze_text

# Page Config
st.set_page_config(page_title="Text Analyzer Pro", layout="wide")

st.title("📄 Multi-Format Text Analyzer")
st.markdown("Upload a **PDF, DOCX, or TXT** file to analyze its content instantly.")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    # 1. Extract Text
    with st.spinner("Extracting text..."):
        raw_text = extract_text(uploaded_file)
    
    if raw_text:
        # 2. Run Analysis
        analysis = analyze_text(raw_text)
        
        # 3. Display Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Word Count", analysis["word_count"])
        col2.metric("Character Count", analysis["char_count"])
        col3.metric("Sentiment", analysis["sentiment_label"], delta=analysis["sentiment_score"])
        
        # 4. Show Content Tabs
        tab1, tab2 = st.tabs(["Raw Content", "Key Insights"])
        
        with tab1:
            st.text_area("File Content", raw_text, height=300)
            
        with tab2:
            st.subheader("Text Preview (First 500 chars)")
            st.write(raw_text[:500] + "...")
            
            # Export Option
            st.download_button("Download Raw Text", raw_text, file_name="extracted_text.txt")
    else:
        st.error("Could not read the file. Please check the format.")
