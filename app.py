import streamlit as st
import pandas as pd
import json
from utils import extract_text, analyze_text, get_summary, get_keywords, extract_text_from_url

# 1. Page Config (MUST be at the very top)
st.set_page_config(page_title="Ultimate Text Analyzer Pro", layout="wide", page_icon="📄")

st.title("🚀 Full-Fledged AI Text Analyzer")
st.markdown("Analyze documents, images, spreadsheets, or even live websites in seconds.")

# 2. Sidebar for Input Selection
with st.sidebar:
    st.header("Settings")
    input_source = st.radio("Select Input Source:", ["📁 Upload File", "🌐 Analyze Website"])
    st.info("Supported: PDF, DOCX, TXT, CSV, XLSX, PNG, JPG")

raw_text = ""

# 3. Handle Input Sources
if input_source == "📁 Upload File":
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt", "csv", "xlsx", "png", "jpg", "jpeg"])
    if uploaded_file:
        with st.spinner("🔍 Processing file..."):
            raw_text = extract_text(uploaded_file)
else:
    url = st.text_input("Enter Website URL (e.g., https://google.com)")
    if url:
        with st.spinner("🌐 Scraping website..."):
            raw_text = extract_text_from_url(url)

# 4. Main Analysis Logic
if raw_text:
    # Check if we got an error message from the scraper/extractor
    if raw_text.startswith("Error"):
        st.error(raw_text)
    else:
        # Initialize variables
        summary_points = []
        keywords = []
        
        # Setup Tabs
        tab1, tab2 = st.tabs(["📁 Data Content", "📊 Analysis Insights"])
        
        with tab1:
            if raw_text.startswith("TABLE_DATA|"):
                data = json.loads(raw_text.split("|")[1])
                df = pd.DataFrame(data)
                st.dataframe(df, width='stretch')
            else:
                st.text_area("Extracted Content", raw_text, height=400)
            
        with tab2:
            if raw_text.startswith("TABLE_DATA|"):
                st.subheader("📋 Spreadsheet Insights")
                data = json.loads(raw_text.split("|")[1])
                df = pd.DataFrame(data)
                
                st.write(f"🔹 **Total Records:** {len(df)} rows")
                st.write(f"🔹 **Columns Found:** {', '.join(df.columns)}")
                st.subheader("📈 Column Statistics")
                st.write(df.describe(include='all').transpose())
                
                summary_points = [f"Table with {len(df)} rows and {len(df.columns)} columns."]
                keywords = list(df.columns[:5])
            else:
                # Narrative Analysis
                analysis = analyze_text(raw_text)
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Word Count", analysis["word_count"])
                col2.metric("Sentiment", analysis["sentiment_label"], delta=analysis["sentiment_score"])
                
                st.subheader("📋 Key Takeaways")
                summary_points = get_summary(raw_text)
                for point in summary_points:
                    st.write(f"🔹 {point}")
                
                st.subheader("🔑 Top Keywords")
                keywords = get_keywords(raw_text)
                if keywords:
                    st.markdown(" ".join([f"`{w.upper()}`" for w in keywords]))

        # 5. Export Section
        st.divider()
        bullet_summary = "\n".join([f"- {p}" for p in summary_points])
        analysis_data = f"TEXT ANALYSIS REPORT\n{'='*20}\n\nSUMMARY:\n{bullet_summary}\n\nKEYWORDS: {', '.join(keywords)}"
        st.download_button("📩 Download Full Report", analysis_data, file_name="analysis_report.txt")
else:
    st.write("---")
    st.info("Waiting for input... Please upload a file or enter a URL to begin analysis.")
