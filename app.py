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
            
        # ... (inside the Key Insights tab)
        with tab2:
            st.subheader("🤖 AI-Generated Summary")
            summary = get_summary(raw_text)
            st.info(summary)
            
            st.subheader("🔑 Top Keywords")
            keywords = get_keywords(raw_text)
            cols = st.columns(len(keywords))
            for i, word in enumerate(keywords):
                cols[i].button(word, key=i) # Displays keywords as clickable tags

            # Export Option
            st.divider()
            st.download_button("Download Full Analysis", f"Summary:\n{summary}\n\nKeywords: {', '.join(keywords)}", file_name="analysis.txt")
    else:
        st.error("Could not read the file. Please check the format.")
