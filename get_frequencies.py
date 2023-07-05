#! /usr/local/python/current/bin/python

from nltk.tokenize import word_tokenize
from src import Corpus
from pathlib import Path
from collections import Counter
import pandas as pd
import json
from src import preprocess

if __name__ == "__main__":
    abstracts = Corpus(Path("data/raw/abstracts"))
    eudract = Corpus(Path("data/raw/eudract"))
    cwlsc = Corpus(Path("data/raw/cwlsc"))
    mentions = abstracts.mentions + eudract.mentions + cwlsc.mentions
    vocabulary = {}
    for mention in mentions:
        try:
            tokenized_mention = word_tokenize(mention[2])
        except LookupError:
            import nltk
            nltk.download('punkt')
            tokenized_mention = word_tokenize(mention[2])
        corpus = mention[1]
        for word in tokenized_mention:
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
    frequencies = frequencies.melt(var_name="corpus",value_name="frequency", ignore_index=False)
    frequencies.sort_values(["corpus"], inplace=True)
    frequencies.sort_index(inplace=True)
    frequencies.to_excel("data/processed/frequencies.xlsx", index_label="word")