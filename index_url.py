#Libraries
import requests
from bs4 import BeautifulSoup

def url_context(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    extracted_text = ' '.join([para.get_text() for para in paragraphs])
    return extracted_text
