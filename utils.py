import os
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob
from jinja2 import Environment, FileSystemLoader
import pdfkit


def summarize_text(text):
    blob = TextBlob(text)
    return str(blob.sentences[0]) if blob.sentences else "No summary available."


def extract_keywords(text):
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform([text])
    keywords = vectorizer.get_feature_names_out()
    freqs = X.toarray()[0]
    data = dict(zip(keywords, freqs))
    return sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]


def generate_wordcloud(text):
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    path = 'smart_report_generator/static/wordcloud.png'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wc.to_file(path)
    return path


def generate_keyword_graph(keyword_data):
    words, counts = zip(*keyword_data)
    plt.figure(figsize=(8, 4))
    sns.barplot(x=list(counts), y=list(words), palette="viridis")
    plt.title("Top Keywords Frequency")
    plt.xlabel("Count")
    plt.tight_layout()
    path = "smart_report_generator/static/keyword_freq_plot.png"
    plt.savefig(path)
    plt.close()
    return path


def generate_sentiment_graph(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    plt.figure(figsize=(4, 3))
    plt.bar(["Sentiment"], [polarity], color="skyblue")
    plt.ylim(-1, 1)
    plt.axhline(0, color="gray", linestyle="--")
    plt.title("Overall Sentiment Polarity")
    path = "smart_report_generator/static/sentiment_plot.png"
    plt.savefig(path)
    plt.close()
    return path


def render_report(summary, keywords, wordcloud_img, keyword_plot, sentiment_plot):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(base_dir, "templates")
    output_dir = os.path.join(base_dir, "output")

    os.makedirs(output_dir, exist_ok=True)

    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("report_template.html")

    html_out = template.render(
        summary=summary,
        keywords=keywords,
        wordcloud_img=wordcloud_img,
        keyword_plot=keyword_plot,
        sentiment_plot=sentiment_plot
    )

    html_path = os.path.join(output_dir, "report.html")
    pdf_path = os.path.join(output_dir, "report.pdf")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_out)

    # Configure pdfkit
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    options = {
    'enable-local-file-access': ''
    }
    pdfkit.from_file(html_path, pdf_path, options=options, configuration=config)

    return pdf_path
