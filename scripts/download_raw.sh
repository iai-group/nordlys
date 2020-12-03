# Script for downloading the raw data files needed by Nordlys

# FACC
echo "############ Downloading FACC file..."
DIR=data/raw-data/facc
wget --directory-prefix=$DIR/ https://iai.group/downloads/nordlys-v02/clueweb12_facc1_counts.bz2
echo "############ Done."

# Word2vec
echo "############ Downloading Word2vec embeddings file..."
DIR=data/raw-data/word2vec
wget --directory-prefix=$DIR/ https://iai.group/downloads/nordlys-v02/googlenews-vectors-negative300.txt.bz2
echo "############ Done."