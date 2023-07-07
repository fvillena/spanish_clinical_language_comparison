#! /usr/local/python/current/bin/python

from nltk.tokenize import word_tokenize
from src import Corpus
from pathlib import Path
from collections import Counter
import pandas as pd
import json
from src import preprocess
from sklearn.preprocessing import QuantileTransformer
import numpy as np

if __name__ == "__main__":
    abstracts = Corpus(Path("data/raw/abstracts"))
    eudract = Corpus(Path("data/raw/eudract"))
    cwlsc = Corpus(Path("data/raw/cwlsc"))
    texts = abstracts.txts + eudract.txts + cwlsc.txts
    vocabulary = {}
    for text in texts:
        try:
            tokens = word_tokenize(str(text))
        except LookupError:
            import nltk
            nltk.download('punkt')
            tokens = word_tokenize(str(text))
        corpus = text.corpus
        for word in tokens:
            word = preprocess(word)
            if word in vocabulary:
                vocabulary[word].update([corpus])
            else:
                vocabulary[word] = Counter([corpus])
    with open('data/interim/unigrams.json') as f:
        unigram_frequency = json.load(f)
    unigram_frequency_processed = {}
    for word,frequency in unigram_frequency.items():
        if word in unigram_frequency_processed:
            unigram_frequency_processed[word] + frequency
        else:
            unigram_frequency_processed[word] = frequency
    with open('data/interim/umls_unigrams.json') as f:
        umls_unigram_frequency = json.load(f)
    for word,counter in vocabulary.items():
        try:
            counter.update(google = unigram_frequency_processed[word])
            counter.update(umls = umls_unigram_frequency[word])
        except:
            continue
    frequencies = pd.DataFrame.from_dict(vocabulary, orient="index").fillna(0)
    scaler = QuantileTransformer(n_quantiles=10000)
    frequencies_scaled = frequencies.applymap(lambda x: np.log2(x+1))
    frequencies_scaled[:] = scaler.fit_transform(frequencies)
    frequencies = frequencies.melt(var_name="corpus",value_name="frequency", ignore_index=False).reset_index(names="word")
    frequencies_scaled = frequencies_scaled.melt(var_name="corpus",value_name="frequency_scaled", ignore_index=False).reset_index(names="word")
    frequencies = frequencies.merge(frequencies_scaled, on=["word","corpus"])
    frequencies.sort_values(["word","corpus"], inplace=True)
    frequencies.to_excel("data/processed/frequencies.xlsx", index=False)