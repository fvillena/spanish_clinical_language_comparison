#! /usr/local/python/current/bin/python

import dask.dataframe as dd

unigrams = dd.read_csv("data/raw/google-unigrams/*.gz",
                       sep="\t", header=None, 
                       names=["unigram", "year", "frequency", 'books'], 
                       dtype = {"unigram":str},
                       compression='gzip', blocksize=None)

result = unigrams.groupby(["unigram"]).frequency.sum().compute()
result.to_json("data/interim/unigrams.json")
