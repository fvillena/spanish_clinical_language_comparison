#! /usr/local/python/current/bin/python

from src import Corpus
import pandas as pd
from pathlib import Path
from src import preprocess

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mrsty", default=None, help="Path to MRSTY", type=Path)
    args = parser.parse_args()
    abstracts = Corpus(Path("data/raw/abstracts"))
    eudract = Corpus(Path("data/raw/eudract"))
    cwlsc = Corpus(Path("data/raw/cwlsc"))
    mentions = abstracts.mentions + eudract.mentions + cwlsc.mentions
    data = pd.DataFrame(mentions, columns = ["code","corpus","text"])
    data["text"] = data.text.apply(preprocess)
    data = data.groupby(["code","corpus","text"]).size().reset_index().rename(columns={0:"frequency"})
    if args.mrsty:
        import csv
        semantic_type = {}
        with open(args.mrsty, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                cui = row[0]
                sty = row[3]
                if cui not in semantic_type:
                    semantic_type[cui] = sty
                else:
                    semantic_type[cui] += f" | {sty}"
        data["semantic_type"] = data.code.apply(lambda x: semantic_type[x] if x in semantic_type else None)
    data.sort_values(["code","corpus","frequency"], inplace=True)
    data.to_excel("data/processed/mentions.xlsx", index=False)