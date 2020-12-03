# Scipt for downloading auxiliary Nordlys files

# Type-to-entity mapping
echo "############ Downloading type-to-entity mapping file..."
DIR=data/raw-data/dbpedia-2015-10/type2entity-mapping
if [ -f $DIR/dbpedia-2015-10-type_to_entity.csv.bz2 ]
then
    echo "$DIR/dbpedia-2015-10-type_to_entity.csv.bz2 has already been downloaded."
else
    wget --directory-prefix=$DIR/ https://iai.group/downloads/nordlys-v02/dbpedia-2015-10-type_to_entity.csv.bz2
fi
echo "############ Done."

# Freebase-to-DBpedia mapping
echo "############ Downloading Freebase to DBpedia mapping files..."
DIR=data/raw-data/dbpedia-2015-10/freebase2dbpedia
wget --directory-prefix=$DIR/ http://downloads.dbpedia.org/2015-10/core-i18n/en/freebase_links_en.ttl.bz2
wget --directory-prefix=$DIR/ http://downloads.dbpedia.org/3.9/links/freebase_links.nt.bz2
echo "############ Done."

# Entity snapshot
echo "############ Downloading Entity snapshot file..."
DIR=data/el
wget --directory-prefix=$DIR/  https://iai.group/downloads/nordlys-v02/snapshot_2015_10.txt
echo "############ Done."
