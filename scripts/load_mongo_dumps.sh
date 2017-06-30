# check whether mongodb is running or not.
mongo --eval "db.stats()"
RESULT=$?
if [ $RESULT -ne 0 ]; then
    echo "mongodb not running"
    exit 1 # if mongodb not running then exit
else
    echo "mongodb running!"
fi

# get current path of this script
dir=$(pwd)

# make a tmp folder to store data
mkdir -p $dir/tmp

# Download all mongodb collections
echo "\n############ Start to download all mongodb collections"
if [ -f $dir/tmp/surface_forms_dbpedia.tar.bz2 ]
then
    echo "$dir/tmp/surface_forms_dbpedia.tar.bz2 has been downloaded."
else
    wget http://iai.group/downloads/nordlys-v02/surface_forms_dbpedia.tar.bz2 -P $dir/tmp/
fi

if [ -f $dir/tmp/surface_forms_facc.tar.bz2 ]
then
    echo "$dir/tmp/surface_forms_facc.tar.bz2 has been downloaded."
else
    wget http://iai.group/downloads/nordlys-v02/surface_forms_facc.tar.bz2 -P $dir/tmp/
fi

if [ -f $dir/tmp/fb2dbp-2015-10.tar.bz2 ]
then
    echo "$dir/tmp/fb2dbp-2015-10.tar.bz2 has been downloaded."
else
    wget http://iai.group/downloads/nordlys-v02/fb2dbp-2015-10.tar.bz2 -P $dir/tmp/
fi

if [ -f $dir/tmp/word2vec-googlenews.tar.bz2 ]
then
    echo "$dir/tmp/word2vec-googlenews.tar.bz2 has been downloaded."
else
    wget http://iai.group/downloads/nordlys-v02/word2vec-googlenews.tar.bz2 -P $dir/tmp/
fi

echo "############ Mongodb collections download end"

# uncompress data
echo "\n############ Start to uncompress data"
mkdir -p $dir/tmp/surface_forms_dbpedia
tar -xjvf $dir/tmp/surface_forms_dbpedia.tar.bz2 -C $dir/tmp/surface_forms_dbpedia

mkdir -p $dir/tmp/surface_forms_facc
tar -xjvf $dir/tmp/surface_forms_facc.tar.bz2 -C $dir/tmp/surface_forms_facc

mkdir -p $dir/tmp/fb2dbp-2015-10
tar -xjvf $dir/tmp/fb2dbp-2015-10.tar.bz2 -C $dir/tmp/fb2dbp-2015-10

mkdir -p $dir/tmp/word2vec-googlenews
tar -xjvf $dir/tmp/word2vec-googlenews.tar.bz2 -C $dir/tmp/word2vec-googlenews
echo "############ Data uncompressed"

# load all collections into mongodb
echo "Start to load collections into mongodb"
mongorestore --db "nordlys-v02" $dir/tmp/surface_forms_dbpedia
mongorestore --db "nordlys-v02" $dir/tmp/surface_forms_facc
mongorestore --db "nordlys-v02" $dir/tmp/fb2dbp-2015-10
mongorestore --db "nordlys-v02" $dir/tmp/word2vec-googlenews
echo "Collections loaded"

# remove tmp folder
rm -rf $dir/tmp/

# Load DBpedia to MongoDB
cd ..
python -m nordlys.core.data.dbpedia.dbpedia2mongo data/config/dbpedia2mongo.config.json
