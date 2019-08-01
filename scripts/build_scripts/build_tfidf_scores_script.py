import random
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import re
import pandas as pd
from RevolicoProject.DataSets import DataSetProvider
from RevolicoProject.ModelBuilding import Lemmatizer
from nltk.stem import SnowballStemmer
from nltk import word_tokenize

# dataSet = DataSetProvider(3, 'filekk')

# print(dataSet.amount)

dataFile = '/home/gauss/arm/importante/work/ai/projects/revolico/clean_data/ads_dump.csv'

df = pd.read_csv(dataFile)  # [0:10000]
print('Amount of data', df.shape[0])
# df = df.sample(n=100).reset_index(drop=True)

lemma = Lemmatizer()


def pre_process(text):
    text = str(text)
    # lowercase
    text = text.lower()
    # remove special characters and digits
    text = re.sub("(\\d|\\W)+", " ", text)

    # stem
    # stemmer = SnowballStemmer('spanish')
    # tokens = word_tokenize(text)
    # stemmedTokens = [stemmer.stem(token) for token in tokens]
    # text = ' '.join(stemmedTokens)
    # lemmatize
    tokens = word_tokenize(text)
    lemmaTokens = [lemma.lemmatize(token) for token in tokens]
    text = ' '.join(lemmaTokens)

    return text


df['text'] = df['title'] + ' ' + df['content']
df['text'] = df['text'].apply(lambda x: pre_process(x))

# show the second 'text' just for fun
# print(df['text'][2])


def get_stop_words(stop_file_path):
    """load stop words """

    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)


# load a set of stop words
stopwords = get_stop_words(
    "/home/gauss/arm/importante/work/ai/projects/revolico/revolico_code/resources/stopwords-revolico.txt")

# get the text column
docs = df['text'].tolist()
print(docs[0])

# create a vocabulary of words,
# ignore words that appear in 85% of documents,
# eliminate stop words
cv = CountVectorizer(max_df=0.95, stop_words=stopwords)
word_count_vector = cv.fit_transform(docs)

# cv = CountVectorizer(max_df=0.85, stop_words=stopwords, max_features=10000)
# word_count_vector = cv.fit_transform(docs)

print('First ten words', list(cv.vocabulary_.keys())[:10])


tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
tfidf_transformer.fit(word_count_vector)


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""

    # use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:

        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results


feature_names = cv.get_feature_names()

# get the document that we want to extract keywords from
# doc = docs[0]
# print(doc)
# docsToShow = random.sample(docs, 20)
sampleDF = df.sample(n=20).reset_index(drop=True)
sampleDF['title'] = sampleDF['title'].apply(lambda x: pre_process(x))
titles = sampleDF['title'].tolist()
texts = sampleDF['text'].tolist()
docs = zip(titles, texts)
for title, doc in docs:
    # generate tf-idf for the given document
    tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))

    # sort the tf-idf vectors by descending order of scores
    sorted_items = sort_coo(tf_idf_vector.tocoo())

    # extract only the top n; n here is 10
    keywords = extract_topn_from_vector(feature_names, sorted_items, 10)

    # now print the results
    print("\n=====Doc=====")
    print(title)
    print("\n===Keywords===")
    for k in keywords:
        if k in title:
            print(k, keywords[k])
