#! /usr/local/python/current/bin/python

import pandas as pd
from nltk.tokenize import word_tokenize
from src import preprocess
import json
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

data = pd.read_csv('data/raw/MRCONSO_202307050503.csv')

cv = CountVectorizer(
    preprocessor=preprocess,
    tokenizer=word_tokenize
)

x = cv.fit_transform(data.STR)


vocab = list(cv.get_feature_names_out())
count = dict(zip(vocab, x.sum(axis=0).A1))

with open("data/interim/umls_unigrams.json", mode="w", encoding="utf-8") as f:
    f.write(json.dumps(count, ensure_ascii=False, cls=NpEncoder))
