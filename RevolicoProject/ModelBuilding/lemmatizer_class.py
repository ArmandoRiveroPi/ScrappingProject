import pickle
from nltk import word_tokenize
lemmaDicFile = '/home/gauss/arm/importante/work/ai/projects/revolico/revolico_code/RevolicoProject/ModelBuilding/lemma-dic.pickle'


class Lemmatizer(object):
    def __init__(self):
        dicFile = open(lemmaDicFile, 'rb')
        self.lemmaDic = pickle.loads(dicFile.read())

    def lemmatize_word(self, word):
        if word in self.lemmaDic:
            return self.lemmaDic[word]
        else:
            return word

    def lemmatize_text(self, text):
        tokens = word_tokenize(text)
        lemmaTokens = [self.lemmatize_word(token) for token in tokens]
        text = ' '.join(lemmaTokens)
        return text
