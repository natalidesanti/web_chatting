#Libraries
from transformers import pipeline
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

def ask_question(context, question):
    QA = pipeline('question-answering', model = 'distilbert-base-cased-distilled-squad')
    return QA({'context': context, 'question': question})['answer']

@app.route('/ask', methods = ['POST'])
def ask():
    
    data = request.json
    url = data.get('url')
    question = data.get('question')

    if not url or not question:
        return jsonify({'error': 'Please provide a URL and a question'}), 400

    #Content from the first API
    content_from_url = requests.post('http://127.0.0.1:5001/url_context', json = {'url': url})

    if content_from_url.status_code != 200:
        return jsonify({'error': 'Failed to fetch content'}), 500

    content = content_from_url.json().get('content')
    answer = ask_question(content, question)

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(port = 5000, debug = True)

