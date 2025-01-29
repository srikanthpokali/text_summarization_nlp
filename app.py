from flask import Flask, render_template, request, jsonify
import spacy
from transformers import pipeline

# Load NLP models
nlp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization")

app = Flask(__name__)

def extractive_summary(text, num_sentences=3):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    return " ".join(sentences[:num_sentences])

def abstractive_summary(text):
    return summarizer(text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ""
    if request.method == 'POST':
        text = request.form['text']
        method = request.form['method']
        
        if method == 'extractive':
            summary = extractive_summary(text)
        else:
            summary = abstractive_summary(text)
    
    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
