
import streamlit as st
from utils import summarize_text, extract_keywords, generate_wordcloud, generate_keyword_graph, generate_sentiment_graph, render_report

st.set_page_config(page_title="Smart Report Generator", layout="centered")
st.title("📄 Smart Report Generator")
st.write("Upload a text file to generate a neat report with summaries, keywords, and visualizations.")

uploaded_file = st.file_uploader("Upload your .txt file", type=["txt"])

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
    with open("sample_input.txt", "w") as f:
        f.write(text)

    summary = summarize_text(text)
    keywords = extract_keywords(text)
    wordcloud_img = generate_wordcloud(text)
    keyword_plot = generate_keyword_graph(keywords)
    sentiment_plot = generate_sentiment_graph(text)

    render_report(summary, keywords, wordcloud_img, keyword_plot, sentiment_plot)

    st.success("✅ Report generated!")

    st.subheader("📌 Keywords")
    st.dataframe(keywords, use_container_width=True)

    st.subheader("🎨 Wordcloud")
    st.image(wordcloud_img)

    st.subheader("📊 Keyword Frequency")
    st.image(keyword_plot)

    st.subheader("💬 Sentiment Analysis")
    st.image(sentiment_plot)

    st.subheader("📥 Download Report")
    with open("output/report.pdf", "rb") as f:
        st.download_button("Download PDF Report", f, file_name="smart_report.pdf")
