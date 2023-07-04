#! /bin/bash

wget -nc -P /tmp http://www.lllf.uam.es/ESP/nlpdata/wp2/CT-EBM-SP.zip
unzip -j /tmp/CT-EBM-SP.zip "train/abstracts/*" -d ./data/raw/abstracts
unzip -j /tmp/CT-EBM-SP.zip "train/eudract/*" -d ./data/raw/eudract
wget -nc -P /tmp https://zenodo.org/record/7757971/files/CWLsC.zip
unzip -j /tmp/CWLsC.zip "CWLsC/ann/*" -d ./data/raw/cwlsc
google-ngram-downloader download -l spa -o data/raw/google-unigrams