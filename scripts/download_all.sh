# Script for downloading the raw files needed by Nordlys

# ---
# DBpedia 2015-10 collection
echo "############ Downloading DBpedia files needed by Nordlys ..."
DIR=data/raw-data/dbpedia-2015-10/core-i18n/en
rm  $DIR/*.bz2
wget --directory-prefix=$DIR/ -i $DIR/nordlys_dbpedia_2015_10-raw_data_links-core.txt
echo "############ Done."

# ---
# Type-to-entity mapping
echo "############ Downloading type-to-entity file..."
DIR=data/raw-data/dbpedia-2015-10/type2entity-mapping
wget --directory-prefix=$DIR/ -i $DIR/http://iai.group/downloads/nordlys-v02/dbpedia-2015-10-type_to_entity.csv.bz2
echo "############ Done."

# ---
# Freebase to DBpedia
echo "############ Downloading Freebase to DBpedia files..."
DIR=data/raw-data/dbpedia-2015-10/freebase2dbpedia
wget --directory-prefix=$DIR/ -i http://downloads.dbpedia.org/2015-10/core-i18n/en/freebase_links_en.ttl.bz2
wget --directory-prefix=$DIR/ -i http://downloads.dbpedia.org/3.9/links/freebase_links.nt.bz2
echo "############ Done."


# ---
# FACC
echo "############ Downloading FACC file..."
DIR=data/raw-data/facc
wget --directory-prefix=$DIR/ -i http://iai.group/downloads/nordlys-v02/clueweb12_facc1_counts.bz2
echo "############ Done."


# ---
# Word2Vec
echo "############ Downloading word2vec embeddings file..."
DIR=data/raw-data/word2vec
wget --directory-prefix=$DIR/ -i http://iai.group/downloads/nordlys-v02/googlenews-vectors-negative300.txt.bz2
echo "############ Done."
