# Script for downloading a specific version of DBpedia (2015-10 or 2016-10)

VERSION=2015-10

DIR=data/raw-data/dbpedia-$VERSION/core-i18n/en
mkdir -p DIR

echo "############ Downloading DBpedia $VERSION files needed by Nordlys..."
wget --directory-prefix=$DIR/ -i $DIR/dbpedia_files.txt
echo "############ Done."
