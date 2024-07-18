#Libraries
from transformers import pipeline

def ask_question(context, question):
    QA = pipeline('question-answering', model = 'distilbert-base-cased-distilled-squad')
    return QA({'context': context, 'question': question})['answer']
