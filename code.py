import streamlit as st
from utils import extract_text, analyze_text, get_summary, get_keywords
import pandas as pd

# Page Config
st.set_page_config(page_title="Text Analyzer Pro", layout="wide")

st.title("📄 Multi-Format Text Analyzer")
st.markdown("Upload a **PDF, DOCX, or TXT** file to analyze its content instantly.")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt", "csv", "xlsx"])

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
        tab1, tab2 = st.tabs(["📁 Data Preview", "📊 Analysis Results"])
        
        with tab1:
            if raw_text.startswith("TABLE_DATA|"):
                # Convert back to DataFrame for display
                import json
                data = json.loads(raw_text.split("|")[1])
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
            else:
                st.text_area("File Content", raw_text, height=300)
            
        with tab2:
            if raw_text.startswith("TABLE_DATA|"):
                st.subheader("📋 Spreadsheet Insights")
                import json
                data = json.loads(raw_text.split("|")[1])
                df = pd.DataFrame(data)
                
                st.write(f"🔹 **Total Records:** {len(df)} rows")
                st.write(f"🔹 **Columns Found:** {', '.join(df.columns)}")
                
                st.subheader("📈 Column Statistics")
                st.write(df.describe(include='all').transpose())
            else:
                # Use your existing summary_points logic for PDF/DOCX
                st.subheader("📋 Key Takeaways")
                summary_points = get_summary(raw_text)
                for point in summary_points:
                    st.write(f"🔹 {point}")
            
            st.divider()
            
            st.subheader("🔑 Document Keywords")
            keywords = get_keywords(raw_text)
            if keywords:
                # Displays keywords as non-clickable 'tags' using markdown
                keyword_tags = " ".join([f"`{word.upper()}`" for word in keywords])
                st.markdown(keyword_tags)
                          
            # Export Option
            st.write("")
            bullet_summary = "\n".join([f"- {p}" for p in summary_points])
            analysis_data = f"TEXT ANALYSIS REPORT\n{'='*20}\n\nSUMMARY:\n{bullet_summary}\n\nTOP KEYWORDS: {', '.join(keywords)}"
            st.download_button("📩 Download Full Report", analysis_data, file_name="analysis_report.txt")
    else:
        st.error("Could not read the file. Please check the format.")
