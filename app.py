import streamlit as st
from utils import extract_text, analyze_text, get_summary, get_keywords

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
            st.subheader("📋 Key Takeaways & Summary")
            
            summary_points = get_summary(raw_text)
            
            # Displaying the summary points in a nice container
            with st.container():
                for point in summary_points:
                    if len(point) > 5: # Avoid empty bullets
                        st.markdown(f"**•** {point}")
            
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
