# Downloads a specific version of DBpedia:
# 2015-10 (default) or 2016-10 (if provided as 1st argument)

VERSION=2015-10
if [ $1 = "2016-10" ]; then
  VERSION=2016-10
fi

DIR=data/raw-data/dbpedia-$VERSION
mkdir -p DIR

echo "############ Downloading DBpedia $VERSION files needed by Nordlys to $DIR..."
wget --directory-prefix=$DIR/core-i18n/en -i $DIR/dbpedia_files.txt
echo "############ Done."
