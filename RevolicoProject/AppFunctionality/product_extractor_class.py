from ..ModelBuilding import TfidfProvider
from ..functions import dict_average
import spacy
import re


class ProductExtractor(object):
    """Handles the extraction of product names and prices from an ad
    """

    def __init__(self):
        self.nlp = spacy.load('es_core_news_md')
        self.tfidf = TfidfProvider()

    def pre_process(self, text):
        text = str(text)
        # lowercase
        text = text.lower()
        # remove special characters double spaces
        text = re.sub(r'\W+', " ", text)
        text = re.sub(r'\s+', " ", text)
        return text

    def get_nouns(self, text):
        cleanText = self.pre_process(text)
        parsedText = self.nlp(cleanText)
        print('Clean text -->', cleanText)
        print('POS Tokens', '>'*50)
        for token in parsedText:
            # if token.pos_ == 'NOUN':
            print(token.text, token.pos_, token.dep_, token.lemma_)

        # print('ENTITIES', '>'*50)
        # for ent in parsedText.ents:
        #     print(ent.text, ent.start_char, ent.end_char, ent.label_)

        nouns = [token.text for token in parsedText if token.pos_ ==
                 'NOUN' and not re.match(r'^\d+$', token.text)]
        return nouns

    def extract_product(self, adDic):
        title = adDic['title']
        content = str(adDic['title']) + ' ' + str(adDic['content'])
        print('Tfidf', self.tfidf.get_text_tfidf(content, title))
        print('Average TFIDF', dict_average(
            self.tfidf.get_text_tfidf(content, content)))
        nouns = self.get_nouns(adDic['title'])
        product = (' '.join(nouns), adDic['price'])
        return product
