# Script for downloading the raw files needed by Nordlys

# ---
# Type-to-entity mapping sample
echo "############ Downloading files needed for building the type index..."
DIR=data/raw-data/dbpedia-2015-1010_sample/core-i18n/en
if [ -f $DIR/short_abstracts_en.ttl.bz2 ]
then
    echo "$DIR/short_abstracts_en.ttl.bz2 has already been downloaded."
else
    wget --directory-prefix=$DIR/ http://downloads.dbpedia.org/2015-10/core-i18n/en/short_abstracts_en.ttl.bz2
fi
DIR=data/raw-data/dbpedia-2015-10_sample/type2entity-mapping
if [ -f $DIR/dbpedia-2015-10_sample-type_to_entity.csv.bz2 ]
then
    echo "$DIR/dbpedia-2015-10_sample-type_to_entity.csv.bz2 has already been downloaded."
else
    wget --directory-prefix=$DIR/ http://iai.group/downloads/nordlys-v02/dbpedia-2015-10-type_to_entity.csv.bz2
fi
echo "############ Done."

# ---
# Freebase to DBpedia sample
echo "############ Downloading Freebase to DBpedia files..."
DIR=data/raw-data/dbpedia-2015-10_sample/freebase2dbpedia
wget --directory-prefix=$DIR/ http://downloads.dbpedia.org/2015-10/core-i18n/en/freebase_links_en.ttl.bz2
wget --directory-prefix=$DIR/ http://downloads.dbpedia.org/3.9/links/freebase_links.nt.bz2
echo "############ Done."
# ---





# DBpedia 2015-10 collection full files
echo "############ Downloading DBpedia files needed by Nordlys..."
DIR=data/raw-data/dbpedia-2015-10/core-i18n/en
wget --directory-prefix=$DIR/ -i $DIR/nordlys_dbpedia_2015_10-raw_data_links-core.txt
echo "############ Done."

# ---
# Type-to-entity mapping
echo "############ Downloading files needed for building the type index..."
DIR=data/raw-data/dbpedia-2015-10/core-i18n/en
if [ -f $DIR/short_abstracts_en.ttl.bz2 ]
then
    echo "$DIR/short_abstracts_en.ttl.bz2 has already been downloaded."
else
    wget --directory-prefix=$DIR/ http://downloads.dbpedia.org/2015-10/core-i18n/en/short_abstracts_en.ttl.bz2
fi
DIR=data/raw-data/dbpedia-2015-10/type2entity-mapping
if [ -f $DIR/dbpedia-2015-10-type_to_entity.csv.bz2 ]
then
    echo "$DIR/dbpedia-2015-10-type_to_entity.csv.bz2 has already been downloaded."
else
    wget --directory-prefix=$DIR/ http://iai.group/downloads/nordlys-v02/dbpedia-2015-10-type_to_entity.csv.bz2
fi
echo "############ Done."

# ---
# Freebase to DBpedia
echo "############ Downloading Freebase to DBpedia files..."
DIR=data/raw-data/dbpedia-2015-10/freebase2dbpedia
wget --directory-prefix=$DIR/ http://downloads.dbpedia.org/2015-10/core-i18n/en/freebase_links_en.ttl.bz2
wget --directory-prefix=$DIR/ http://downloads.dbpedia.org/3.9/links/freebase_links.nt.bz2
echo "############ Done."


# ---
# FACC
echo "############ Downloading FACC file..."
DIR=data/raw-data/facc
wget --directory-prefix=$DIR/ http://iai.group/downloads/nordlys-v02/clueweb12_facc1_counts.bz2
echo "############ Done."


# ---
# Word2Vec
echo "############ Downloading word2vec embeddings file..."
DIR=data/raw-data/word2vec
wget --directory-prefix=$DIR/ http://iai.group/downloads/nordlys-v02/googlenews-vectors-negative300.txt.bz2
echo "############ Done."
