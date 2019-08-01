"""This module provides the functionality regarding Tfidf term transformation

It depends on various decisions like the preprocessing done to the text before vectorizing
and of course, it requires a corpus

It provides functions that give you the tfidf of a term or list of terms after it has built its model
"""
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from nltk import word_tokenize
import pandas
import re
from .lemmatizer_class import Lemmatizer
import pickle

# Stop words file
stopFile = "/home/gauss/arm/importante/work/ai/projects/revolico/revolico_code/resources/stopwords-revolico.txt"
# CountVectorizer file
cvFile = "/home/gauss/arm/importante/work/ai/projects/revolico/revolico_code/RevolicoProject/ModelBuilding/tfidf_cv.pickle"
tfidfTransFile = "/home/gauss/arm/importante/work/ai/projects/revolico/revolico_code/RevolicoProject/ModelBuilding/tfidf_trans.pickle"


class TfidfProvider(object):

    def __init__(self):
        self.lemmatizer = Lemmatizer()
        self.df = pandas.DataFrame()
        self.stopWords = frozenset()
        self.get_stop_words(stopFile)
        self.cv = CountVectorizer(max_df=0.95, stop_words=self.stopWords)
        self.tfidfTrans = TfidfTransformer(smooth_idf=True, use_idf=True)
        self.load_model()

    def build_model(self, csvFile, amount=0):
        self.df = pandas.read_csv(csvFile)
        # Resample the dataframe if the amount has been set
        if amount > 0:
            self.df = self.df.sample(n=amount).reset_index(drop=True)
        # Create the text field by merging title and content
        self.df['text'] = self.df['title'] + ' ' + self.df['content']
        # Clean/preprocess the text field
        self.df['text'] = self.df['text'].apply(lambda x: self.preprocess(x))
        # Train the sklearn model
        docList = self.df['text'].tolist()
        docVectors = self.cv.fit_transform(docList)
        self.tfidfTrans.fit(docVectors)
        self.save_model()

    def save_model(self):
        cvString = pickle.dumps(self.cv)
        with open(cvFile, 'wb') as cvPickleFile:
            cvPickleFile.write(cvString)
        tfidfTransString = pickle.dumps(self.tfidfTrans)
        with open(tfidfTransFile, 'wb') as tfidfTransPickleFile:
            tfidfTransPickleFile.write(tfidfTransString)

    def load_model(self):
        try:
            with open(cvFile, 'rb') as readFile:
                self.cv = pickle.loads(readFile.read())
            with open(tfidfTransFile, 'rb') as readFile:
                self.tfidfTrans = pickle.loads(readFile.read())
        except:
            print('Could not load the model')

    def preprocess(self, text):
        text = str(text)
        # lowercase
        text = text.lower()
        # remove special characters and digits
        text = re.sub("(\\d|\\W)+", " ", text)

        # lemmatize
        # TODO make lemmatizer to work on text not tokens
        text = self.lemmatizer.lemmatize_text(text)

        return text

    def get_stop_words(self, stopFile):
        """load stop words """
        with open(stopFile, 'r', encoding="utf-8") as f:
            stopwords = f.readlines()
            stopSet = set(m.strip() for m in stopwords)
        self.stopWords = frozenset(stopSet)
        return self.stopWords

    def get_items_terms(self, sortedItems):
        # def extract_topn_from_vector(feature_names, sorted_items):
        """get the feature names and tf-idf score of top n items"""

        feature_names = self.cv.get_feature_names()

        score_vals = []
        feature_vals = []

        # word index and corresponding tf-idf score
        for idx, score in sortedItems:

            # keep track of feature name and its corresponding score
            score_vals.append(round(score, 3))
            feature_vals.append(feature_names[idx])

        # create a tuples of feature,score
        #results = zip(feature_vals,score_vals)
        results = {}
        for idx in range(len(feature_vals)):
            results[feature_vals[idx]] = score_vals[idx]

        return results

    def sort_coo(self, coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    def get_doc_tfidf_dic(self, doc=''):
        doc = self.preprocess(doc)
        tfidfVector = self.tfidfTrans.transform(self.cv.transform([doc]))
        # sort the tf-idf vectors by descending order of scores
        sortedItems = self.sort_coo(tfidfVector.tocoo())
        # extract only the top n; n here is 10
        termsDic = self.get_items_terms(sortedItems)
        return termsDic

    def get_term_tfidf(self, doc='', term='', termsDic=None):
        term = self.preprocess(term)
        if termsDic == None:
            termsDic = self.get_doc_tfidf_dic(doc)
        if term in termsDic:
            termTfidf = termsDic[term]
        else:
            termTfidf = 0.0
        return termTfidf
        # return {'term': term, 'doc': doc, 'tfidf': termTfidf}

    def get_text_tfidf(self, doc='', text=''):
        text = self.preprocess(text)
        termsList = word_tokenize(text)
        termsDic = self.get_doc_tfidf_dic(doc)
        listTfidf = {term: self.get_term_tfidf(
            '', term, termsDic) for term in termsList}
        return listTfidf
