#! /usr/local/python/current/bin/python

from nltk.tokenize import word_tokenize
from src import preprocess
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from math import ceil
from collections import Counter
import csv

lines = []
N = 0
C = cpu_count()

with open('data/raw/MRCONSO_202307050503.csv', mode='r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    next(reader, None)
    for i,row in enumerate(reader):
        # if i == 1000000:
        #     break
        N += 1
        lines.append(row[1])

BATCH_SIZE = ceil(N/C)

def process(batch, function):
    processed_batch = []
    for element in batch:
        processed_batch.append(function(element))
    return processed_batch


def execute_in_parallel(function, l, max_workers=C, batch_size=BATCH_SIZE):
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        result = []
        futures = []
        for i in range(0, len(l), batch_size):
            batch = l[i:i + batch_size]
            futures.append(executor.submit(process, batch, function))
        for future in as_completed(futures):
            result.extend(future.result())
    return result

preprocessed_lines = execute_in_parallel(preprocess, lines)
tokenized_lines = execute_in_parallel(word_tokenize, preprocessed_lines)
counters = execute_in_parallel(Counter, tokenized_lines)

#sum counters in pair then merge
counter = counters[0]
for c in counters[1:]:
    counter.update(c)

#save counter in json
with open('data/interim/umls_unigrams.json', 'w') as f:
    json.dump(counter, f)
