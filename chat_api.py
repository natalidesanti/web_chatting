#Libraries
import uuid
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

context_store = {}

@app.route('/chat', methods = ['POST'])
def chat():

    data = request.json
    url = data.get('url')
    question = data.get('question')
    session_id = data.get('session_id')

    if not question:
        return jsonify({'error': 'Please provide a question'}), 400
    
    if session_id:
        # Follow-up question
        follow_up_response = requests.post('http://127.0.0.1:5000/follow_up', json = {'session_id': session_id, 'question': question})
        if follow_up_response.status_code != 200:
            return jsonify({'error': 'Failed to process follow-up question'}), 500
        return follow_up_response.json()
    else:
        # Initial question
        if not url:
            return jsonify({'error': 'Please provide a URL for the initial question'}), 400
        
        initial_response = requests.post('http://127.0.0.1:5000/ask', json = {'url': url, 'question': question})
        if initial_response.status_code != 200:
            return jsonify({'error': 'Failed to process initial question'}), 500
        
        return initial_response.json()

if __name__ == '__main__':
    app.run(port = 5002, debug = True)
