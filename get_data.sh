#! /bin/bash

wget -nc -P /tmp http://www.lllf.uam.es/ESP/nlpdata/wp2/CT-EBM-SP.zip
unzip -j /tmp/CT-EBM-SP.zip "train/abstracts/*" -d ./data/raw/abstracts
unzip -j /tmp/CT-EBM-SP.zip "train/eudract/*" -d ./data/raw/eudract
google-ngram-downloader download -l spa -o data/raw/google-unigrams
#google-ngram-downloader readline -n 1 -l spa > data/raw/google-unigrams.tsv