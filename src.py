from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path
import re
from unidecode import unidecode

@dataclass
class Mention():
    label: str
    text: str
    codes: Optional[List[str]] = None
        
class Ann():
    def __init__(self, ann_path: Path):
        self.name = ann_path.stem
        self.mentions = {}
        with open(ann_path, encoding="UTF-8") as f:
            for line in f:
                if line.startswith("T"):
                    match = re.match(r"(.*)\t(.*) .* .*\t(.*)", line)
                    uid, label, text = match.groups()
                    self.mentions[uid] = Mention(label=label,text=text)
                elif line.startswith("#"):
                    match = re.match(r".*\t.* (.*)\t(C\d+)", line)
                    try:
                        uid, codes = match.groups()
                    except AttributeError:
                        print(f"Error in line: {line}")
                        continue
                    codes = codes.split(",")
                    try:
                        self.mentions[uid].codes = codes
                    except KeyError:
                        print(f"Error in line: {line}")
    def __repr__(self):
        return self.name

class Txt():
    def __init__(self, txt_path: Path):
        self.name = txt_path.stem
        self.corpus = None
        with open(txt_path, encoding="UTF-8") as f:
            self.text = f.read()
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.text
    
class Corpus():
    def __init__(self, corpus_path: Path):
        self.anns = []
        self.txts = []
        self.mentions = []
        self.name = corpus_path.stem
        for ann_path in corpus_path.glob("*.ann"):
            ann = Ann(ann_path)
            self.anns.append(ann)
            for m in ann.mentions.values():
                if m.codes:
                    for code in m.codes:
                        self.mentions.append((code,self.name,m.text))
        for txt_path in corpus_path.glob("*.txt"):
            txt = Txt(txt_path)
            txt.corpus = self.name
            self.txts.append(txt)

def preprocess(word):
    return unidecode(word.lower())