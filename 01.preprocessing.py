import json
import math
import string
from collections import Counter
from pathlib import Path

from tqdm import tqdm

# https://countwordsfree.com/stopwords
stop_words = json.load(open('../input/stop-words/stop_words_english.json'))

dataset_dir = Path('../input/yelp-dataset/')
review_json = dataset_dir.joinpath('yelp_academic_dataset_review.json')
assert review_json.is_file()

def precook(text: str):
    """ Remove punctuations,
        make lower cases,
        remove escape characters,
        tokenize by space,
        count words/tokens,
        remove stop words
    """
    # Magic line, see https://stackoverflow.com/a/266162/13358358
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.lower()
    # Magic line, see https://stackoverflow.com/a/57985417/13358358
    text = text.translate(str.maketrans('', '', ''.join([chr(i) for i in range(1, 32)])))
    tokens = text.split(' ')
    token_count = Counter(tokens)
    for sw in stop_words:
        del token_count[sw]
    return token_count

def calculate_tf(token_count: Counter):
    """ Calculate Term Frequency from a text ~ token_count
    """
    total = sum([v for k, v in token_count.items()])
    return {k:v/total for k, v in token_count.items()}
  
def calculate_df(total_docs: int, doc_contain_token_count: Counter):
    """ Calculate Document Frequency
    """
    return {k:v/total_docs for k, v in doc_contain_token_count.items()}
  
def calculate_idf(df: dict):
    """ Calculate Inverse Document Frequency
    """
    return {k:math.log(1/v) for k, v in df.items()}
  
def calculate_tf_idf(tf: dict, idf: dict):
    """ Calculate TF-IDF from a text ~ tf
    """
    return {k: v*idf[k] for k, v in tf.items()}
  
with open(review_json) as fp:
    total_docs = 100
    doc_contain_token_count = Counter()
    meta_doc_list = []
    for i in tqdm(range(total_docs)):
        line = next(fp)
        token_count = precook(json.loads(line)['text'])
        tf = calculate_tf(token_count)
        meta_doc_list.append({'token_count': token_count,
                              'tf': tf})
        for k, v in token_count.items():
            doc_contain_token_count[k] += 1

df = calculate_df(total_docs, doc_contain_token_count)
idf = calculate_idf(df)
for md in meta_doc_list:
    md['tf_idf'] = calculate_tf_idf(md['tf'], df)
