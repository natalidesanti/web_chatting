# Web chatting

This repo is a conversational interface to chat to some URL content

* `index_url`: this API gets URL text
* `ask.py`: this API takes a URL content (from `index_url`) and a question. It uses a pre-trained transformer (`[DistilBERT](https://huggingface.co/distilbert/distilbert-base-cased-distilled-squad)`) to anwer the question based on the context given by the URL. Additionally, it stores the content with a session ID for follow-up questions
* `chat_api` this API is responsible for the conversation. It allows initial questions and questions given the previous context

## Requisites

These are the main `Python` libraries:
* `requests`
* `bs4`
* `flask`
* `transformers`
* `uuid`

You can easily install all of them using `pip install`.

## Usage

You can easily run these codes following the steps:

* Open different terminal windows/tabs in the directory where the scripts are located and run:

`$ python index_url.py`

`$ python ask.py`

`$ python chat_api.py`

The API processes will start on ports 5001, 5000, and 5002 respectivelly.

* You can test the **chat API** using `curl` to send a POST request.
Here I will showcase questions using my [personal page](https://natalidesanti.github.io).
An example of _first question_ can be given by:

`$ curl -X POST -H "Content-Type: application/json" -d '{"url": "https://natalidesanti.github.io", "question": "Who is Natalí de Santi?"}' http://127.0.0.1:5002/chat`

and you would obtain something like

`{

"answer": "a physicist working with Machine Learning",

"session_id": "f6dbcb56-556b-4f6c-9d97-991834e06b22"

}`

that follows for the _answer_ to the question and the _ID_ for follow-up questions that can be made.

* An example of _follow-up_ question can be:

`$ curl -X POST -H "Content-Type: application/json" -d '{"session_id": "f6dbcb56-556b-4f6c-9d97-991834e06b22", "question": "When did she work at Flatiron?"}' http://127.0.0.1:5002/chat`

and you will get

`
{

"answer": "September 2022 to August 2023"

}
`

which is just the _answer_ related to the previous URL.