import streamlit as st
import pandas as pd  # Fixes the 'pd' error
import json
from utils import extract_text, analyze_text, get_summary, get_keywords

# Add a choice at the top
input_source = st.radio("Select Input Source:", ["📁 Upload File", "🌐 Analyze Website"])

raw_text = ""

if input_source == "📁 Upload File":
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt", "csv", "xlsx", "png", "jpg", "jpeg"])
    if uploaded_file:
        with st.spinner("Processing file..."):
            raw_text = extract_text(uploaded_file)

else:
    url = st.text_input("Enter Website URL (e.g., https://example.com)")
    if url:
        with st.spinner("Scraping website..."):
            from utils import extract_text_from_url
            raw_text = extract_text_from_url(url)

# ... (The rest of your analysis tabs logic remains the same) ...

# Page Config
st.set_page_config(page_title="Text Analyzer Pro", layout="wide")

st.title("📄 Multi-Format Text Analyzer")
st.markdown("Upload a **PDF, DOCX, TXT, CSV, or XLSX** file for instant analysis.")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt", "csv", "xlsx"])

if uploaded_file is not None:
    # 1. Extract Text
    with st.spinner("Processing file..."):
        raw_text = extract_text(uploaded_file)
    
    if raw_text:
        # Initialize variables to avoid NameErrors
        summary_points = []
        keywords = []
        
        # 2. Setup Tabs
        tab1, tab2 = st.tabs(["📁 Data Preview", "📊 Analysis Results"])
        
        with tab1:
            if raw_text.startswith("TABLE_DATA|"):
                data = json.loads(raw_text.split("|")[1])
                df = pd.DataFrame(data)
                st.dataframe(df, width='stretch')
            else:
                st.text_area("File Content", raw_text, height=300)
            
        with tab2:
            if raw_text.startswith("TABLE_DATA|"):
                st.subheader("📋 Spreadsheet Insights")
                data = json.loads(raw_text.split("|")[1])
                df = pd.DataFrame(data)
                
                st.write(f"🔹 **Total Records:** {len(df)} rows")
                st.write(f"🔹 **Columns Found:** {', '.join(df.columns)}")
                st.subheader("📈 Statistics")
                st.write(df.describe(include='all').transpose())
                
                # For download report
                summary_points = [f"Table with {len(df)} rows and {len(df.columns)} columns."]
                keywords = list(df.columns[:5])
            else:
                # Narrative Text Analysis
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

            # 3. Export Option (Now safe from NameErrors)
            st.divider()
            bullet_summary = "\n".join([f"- {p}" for p in summary_points])
            analysis_data = f"TEXT ANALYSIS REPORT\n{'='*20}\n\nSUMMARY:\n{bullet_summary}\n\nKEYWORDS: {', '.join(keywords)}"
            st.download_button("📩 Download Full Report", analysis_data, file_name="analysis_report.txt")
    else:
        st.error("Could not read the file. Please check the format.")
