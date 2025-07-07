

import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama
from sentiment import analyze_sentiments

# Streamlit UI
st.title("AI Web Scraper")
url = st.text_input("Enter Website URL")

if st.button("Scrape Website"):
    if url:
        st.write("Scraping the website...")

        dom_content = scrape_website(url, max_pages=50) 
        body_content = extract_body_content(dom_content)
        cleaned_content = clean_body_content(body_content)

        st.session_state.dom_content = cleaned_content
        sentiment_output = analyze_sentiments(cleaned_content)

        with st.expander("View Cleaned Reviews"):
            st.text_area("Raw Reviews",cleaned_content, height=500)

        # Perform sentiment analysis and show results
                # NEW: Perform sentiment analysis and show results
        st.write("🔍 Performing sentiment analysis on each review...")

        sentiment_output = analyze_sentiments(cleaned_content)

        with st.expander("🧠 Sentiment Analysis Results (Per Review)"):
            st.markdown(sentiment_output, unsafe_allow_html=True)

# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            # Parse the content with Ollama
            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_ollama(dom_chunks, parse_description)
            st.write(parsed_result)
