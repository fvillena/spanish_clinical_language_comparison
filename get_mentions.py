from src import Corpus
from unidecode import unidecode
import pandas as pd
from pathlib import Path

if __name__ == "__main__":
    abstracts = Corpus(Path("data/raw/abstracts"))
    eudract = Corpus(Path("data/raw/eudract"))
    mentions = abstracts.mentions + eudract.mentions
    data = pd.DataFrame(mentions, columns = ["code","corpus","text"])
    data["text"] = data.text.str.lower().apply(unidecode)
    data.sort_values(["code","corpus"], inplace=True)
    data.to_csv("data/processed/mentions.csv", index=False)