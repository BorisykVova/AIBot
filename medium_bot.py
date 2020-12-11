import io
import random
import string
import warnings
from pathlib import Path
from typing import Iterable


import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

warnings.filterwarnings('ignore')

nltk.download('popular', quiet=True)

CORPUS_FILE = Path("chatbot.txt")

GREETING_INPUTS = (
    "hello",
    "hi",
    "greetings",
    "sup",
    "what's up",
    "hey",
)
GREETING_RESPONSES = [
    "hi",
    "hey",
    "*nods*",
    "hi there",
    "hello",
    "I am glad! You are talking to me",
]

raw = CORPUS_FILE.read_text(encoding='utf-8', errors='ignore').lower()

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

lemmer = WordNetLemmatizer()


def lem_tokens(tokens: Iterable[str]):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = {ord(punct): None for punct in string.punctuation}


def lem_normalize(text: str):
    return lem_tokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


def greeting(sentence: str) -> str:
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


def response(user_response):
    bot_response = ''
    sent_tokens.append(user_response)

    tfid = TfidfVectorizer(tokenizer=lem_normalize, stop_words='english')
    tfid_vector = tfid.fit_transform(sent_tokens)

    values = cosine_similarity(tfid_vector[-1], tfid_vector)
    index = values.argsort()[0][-2]
    flat = values.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if req_tfidf:
        bot_response += sent_tokens[index]
    else:
        bot_response += 'I am sorry! I do not understand you.'

    return bot_response


def main():
    print("ROBO: My name is Robo. I will answer your queries about Chatbots. "
          "If you want to exit, type Bye!")

    while True:
        user_response = input('YOU: ').lower()

        if user_response == 'bye':
            print('BOT: good bye!')
            return

        if greet := greeting(user_response):
            print(f'BOT: {greet}.')
            continue

        bot_response = response(user_response).replace('.', '.\n')

        print(f'BOT: {bot_response}')
        sent_tokens.remove(user_response)


if __name__ == '__main__':
    main()
