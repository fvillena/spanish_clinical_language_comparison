from nltk.tokenize import word_tokenize
from src import Corpus
from pathlib import Path
from collections import Counter
import pandas as pd
from unidecode import unidecode

if __name__ == "__main__":
    abstracts = Corpus(Path("data/raw/abstracts"))
    eudract = Corpus(Path("data/raw/eudract"))
    mentions = abstracts.mentions + eudract.mentions
    vocabulary = {}
    for mention in mentions:
        try:
            tokenized_mention = word_tokenize(mention[2])
        except LookupError:
            import nltk
            nltk.download('punkt')
        corpus = mention[1]
        for word in tokenized_mention:
            word = unidecode(word.lower())
            if word in vocabulary:
                vocabulary[word].update([corpus])
            else:
                vocabulary[word] = Counter([corpus])
    frequencies = pd.DataFrame.from_dict(vocabulary, orient="index")
    frequencies = frequencies.melt(var_name="corpus",value_name="frequency", ignore_index=False)
    frequencies.sort_values(["corpus"], inplace=True)
    frequencies.sort_index(inplace=True)
    frequencies.to_csv("data/processed/frequencies.csv", index_label="word")