#Libraries
from transformers import pipeline
import requests
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

def ask_question(context, question):
    QA = pipeline('question-answering', model = 'distilbert-base-cased-distilled-squad')
    return QA({'context': context, 'question': question})['answer']

context_store = {}

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

    #
    #Storing context with a session ID
    session_id = data.get('session_id', str(uuid.uuid4()))
    context_store[session_id] = content
    #

    #return jsonify({'answer': answer})
    return jsonify({'answer': answer, 'session_id': session_id})

#
@app.route('/follow_up', methods = ['POST'])
def follow_up_question():
    
    data = request.json
    session_id = data.get('session_id')
    question = data.get('question')
    
    if not session_id or not question:
        return jsonify({'error': 'Please provide a session ID and a question'}), 400
    
    context = context_store.get(session_id)
    if not context:
        return jsonify({'error': 'Invalid session ID'}), 400
    
    answer = ask_question(context, question)
    return jsonify({'answer': answer})
#

if __name__ == '__main__':
    app.run(port = 5000, debug = True)

