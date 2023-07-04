#! /usr/local/python/current/bin/python

from src import Corpus
from unidecode import unidecode
import pandas as pd
from pathlib import Path

if __name__ == "__main__":
    abstracts = Corpus(Path("data/raw/abstracts"))
    eudract = Corpus(Path("data/raw/eudract"))
    cwlsc = Corpus(Path("data/raw/cwlsc"))
    mentions = abstracts.mentions + eudract.mentions + cwlsc.mentions
    data = pd.DataFrame(mentions, columns = ["code","corpus","text"])
    data["text"] = data.text.str.lower().apply(unidecode)
    data = data.groupby(["code","corpus","text"]).size().reset_index().rename(columns={0:"frequency"})
    data.sort_values(["code","corpus","frequency"], inplace=True)
    data.to_excel("data/processed/mentions.xlsx", index=False)