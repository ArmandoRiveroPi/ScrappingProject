from ..ModelBuilding import TfidfProvider
from ..functions import dict_median
from ..DataBase import DataBase
import spacy
import re


class ProductExtractor(object):
    """Handles the extraction of product names and prices from an ad
    """

    def __init__(self):
        self.nlp = spacy.load('es_core_news_sm')
        self.tfidf = TfidfProvider()
        self.db = DataBase()

    def pre_process(self, text):
        text = str(text)
        # lowercase
        text = text.lower()
        # remove special characters double spaces
        text = re.sub(r'\W+', " ", text)
        text = re.sub(r'_+', " ", text)
        text = re.sub(r'\s+', " ", text)
        return text

    def get_nouns(self, text):
        cleanText = self.pre_process(text)
        parsedText = self.nlp(cleanText)
        print('Clean text -->', cleanText)
        # print('POS Tokens', '>'*50)
        # for token in parsedText:
        #     # if token.pos_ == 'NOUN':
        #     print(token.text, token.pos_, token.dep_, token.lemma_)
        # print('Noun chunks', '>'*50)
        # for chunk in parsedText.noun_chunks:
        #     print(chunk.text, chunk.root.text, chunk.root.dep_,
        #           chunk.root.head.text)

        # print('ENTITIES', '>'*50)
        # for ent in parsedText.ents:
        #     print(ent.text, ent.start_char, ent.end_char, ent.label_)

        nouns = [token.text for token in parsedText if token.pos_ ==
                 'NOUN' and not re.match(r'^\d+$', token.text)]
        return nouns

    def get_noun_chunks(self, text):
        cleanText = self.pre_process(text)
        print('Clean text -->', cleanText)

        parsedText = self.nlp(cleanText)
        nounChunks = {
            chunk.text: chunk.root.head.text for chunk in parsedText.noun_chunks if not re.match(r'^\d+$', chunk.text)}
        return nounChunks

    def get_ad_user_names(self, adDic):
        try:
            userID = int(adDic['user'])
            user = self.db.get_user_by_id(userID)
            rawUserNames = [self.pre_process(name)
                            for name in user.name_set.split(',')]
            userNames = []
            for name in rawUserNames:
                userNames += name.split()
        except ValueError:
            userNames = []
        print('User Names', userNames)
        userNames = [name for name in userNames if len(name) > 1]
        return userNames

    def remove_user_names(self, adDic):
        userNames = self.get_ad_user_names(adDic)
        adDic['title'] = self.pre_process(adDic['title'])
        for user in userNames:
            adDic['title'] = adDic['title'].replace(user, '')
        return adDic

    def extract_product(self, adDic):
        adDic = self.remove_user_names(adDic)
        title = adDic['title']
        content = str(adDic['title']) + ' ' + str(adDic['content'])

        print('Tfidf', self.tfidf.get_text_tfidf(content, title))

        medianTfidf = dict_median(self.tfidf.get_text_tfidf(content, content))
        print('Median TFIDF', medianTfidf)
        # nouns = self.get_nouns(adDic['title'])
        nounChunks = self.get_noun_chunks(title)
        print('Noun Chunks', nounChunks)
        product = (' '.join(noun for noun in nounChunks), adDic['price'])
        return product
