#Libraries
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/url_context', methods = ['POST'])
def url_context():

    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'Please provide a URL'}), 400

    context = requests.get(url)
    soup = BeautifulSoup(context.text, 'html.parser')
    paragraphs = soup.find_all('p')
    content = ' '.join([parag.get_text() for parag in paragraphs])
    
    return jsonify({'content': content})

if __name__ == '__main__':
    app.run(port = 5001, debug = True)
