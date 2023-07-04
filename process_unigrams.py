import dask.dataframe as dd

unigrams = dd.read_csv("data/raw/google-unigrams/*.gz",
                       sep="\t", header=None, 
                       names=["unigram", "year", "frequency"], 
                       dtype = {"unigram":str},
                       compression='gzip', blocksize=None)

result = unigrams.groupby(["unigram","year"]).frequency.sum().compute()
result.to_json("data/processed/unigrams.json", encoding="utf-8")
