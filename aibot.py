import re
import string
from operator import itemgetter
from typing import List, Tuple, Iterable, Generator

import nltk
import requests
import bs4 as bs
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

import logger


class AIBot:
    SENTENCE_THRESHOLD = 0.1
    WIKI_API = 'https://en.wikipedia.org/wiki'
    STOP_WORDS = {'stop'}

    punctuation_removal = {
        ord(punctuation): None
        for punctuation in string.punctuation
    }

    def __init__(self, subject: str):
        self.subject = subject
        self.log = logger.get_logger('AIBot')
        self.wnlemmatizer = nltk.stem.WordNetLemmatizer()

    def run_bot(self):
        while True:
            user_input = input('Ask me something: ')
            if user_input in self.STOP_WORDS:
                break

            print(f'Answer: {self.generate_response(user_input)}')

    def fetch_wiki_text(self) -> str:
        url = f'{self.WIKI_API}/{self.subject}'

        self.log.debug(f'Sending request to {url}.')

        response = requests.get(url)

        if response.status_code == 200:
            self.log.debug(f'Got successful response: {response}.')
        else:
            self.log.warning(f'Got bad response: {response}.')

        raw_html = response.text

        article_html = bs.BeautifulSoup(raw_html, 'html.parser')
        article_paragraphs = article_html.find_all('p')

        article_text = ''.join(p.text for p in article_paragraphs).lower()
        return article_text

    @staticmethod
    def split_text(article_text: str) -> Tuple[List[str], List[str]]:
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)

        # Divide to sentence
        article_sentence = nltk.sent_tokenize(article_text)

        # Divide to words
        article_words = nltk.word_tokenize(article_text)
        return article_sentence, article_words

    def generate_response(self, user_input: str) -> str:
        self.log.debug(f'Generating response for {user_input!r}.')

        article_text = self.fetch_wiki_text()
        article_sentence, article_words = self.split_text(article_text)

        sentences = [*article_sentence, user_input]

        word_vectorizer = TfidfVectorizer(
            tokenizer=self._get_processed_text,
            stop_words='english'
        )

        all_word_vectors = word_vectorizer.fit_transform(sentences)
        similarly_vector: np.ndarray = cosine_similarity(all_word_vectors[-1], all_word_vectors).flatten()

        matched_vectors = list(self._filter_sentences(similarly_vector))[:5]

        if matched_vectors:
            response = '. '.join(article_sentence[index].capitalize() for index, _ in matched_vectors)
            self.log.debug(f'Successfully generated response. Found {len(matched_vectors)} for response.')
        else:
            response = "I'm sorry ☹️, I don't know it 🤦🏼‍♂."
            self.log.warning(f'Not found any similar sentences.')

        return response

    def _perform_lemmatization(self, tokens: Iterable[str]) -> List[str]:
        return [self.wnlemmatizer.lemmatize(token) for token in tokens]

    def _get_processed_text(self, document: str):
        return self._perform_lemmatization(
            nltk.word_tokenize(document.lower().translate(self.punctuation_removal))
        )

    def _filter_sentences(self, similarly_vector: np.ndarray) -> Generator[Tuple[int, float], None, None]:
        similarly_vector_indexed = sorted(enumerate(similarly_vector), key=itemgetter(1), reverse=True)
        for index, similarity in similarly_vector_indexed[1:]:
            if similarity >= self.SENTENCE_THRESHOLD:
                yield index, similarity


if __name__ == '__main__':
    bot = AIBot('A*_search_algorithm')
    # print(bot.generate_response('algorithm'))
    bot.run_bot()
