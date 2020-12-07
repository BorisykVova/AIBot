import re
import random
import string
from typing import List, Tuple, Iterable

import nltk
import requests
import bs4 as bs
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


class AIBot:

    WIKI_API = 'https://en.wikipedia.org/wiki'
    STOP_WORDS = {'stop'}

    punctuation_removal = {
        ord(punctuation): None
        for punctuation in string.punctuation
    }

    def __init__(self, subject: str):
        self.subject = subject

        self.wnlemmatizer = nltk.stem.WordNetLemmatizer()

    def run_bot(self):
        while True:
            user_input = input('Ask me something: ')
            if user_input in self.STOP_WORDS:
                break

            print(f'Answer: {self.generate_response(user_input)}')

    def fetch_wiki_text(self) -> str:
        response = requests.get(f'{self.WIKI_API}/{self.subject}')
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
        article_text = self.fetch_wiki_text()
        article_sentence, article_words = self.split_text(article_text)

        sentences = [*article_sentence, user_input]

        word_vectorizer = TfidfVectorizer(
            tokenizer=self._get_processed_text,
            stop_words='english'
        )

        all_word_vectors = word_vectorizer.fit_transform(sentences)
        similarly_vector_values = cosine_similarity(all_word_vectors[-1], all_word_vectors)
        similar_sentence_number = similarly_vector_values.argsort()[0][-2]

        matched_vector = similarly_vector_values.flatten()
        matched_vector.sort()
        vector_matched = matched_vector[-2]

        if vector_matched == 0:
            return "I'm sorry, I could not understand you."
        else:
            return article_sentence[similar_sentence_number]

    def _perform_lemmatization(self, tokens: Iterable[str]) -> List[str]:
        return [self.wnlemmatizer.lemmatize(token) for token in tokens]

    def _get_processed_text(self, document: str):
        return self._perform_lemmatization(
            nltk.word_tokenize(document.lower().translate(self.punctuation_removal))
        )


if __name__ == '__main__':
    bot = AIBot('A*_search_algorithm')
    # print(bot.generate_response('algorithm'))
    bot.run_bot()
