# check whether mongodb is running or not.
mongo --eval "db.stats()"
RESULT=$?
if [ $RESULT -ne 0 ]; then
    echo "mongodb not running"
    exit 1 # if mongodb not running then exit
else
    echo "mongodb running!"
fi

load_collection () {
	mkdir -p $(pwd)/tmp
	dir=$(pwd)/tmp
	wget http://iai.group/downloads/nordlys-v02/$1 -P $dir
	tar -xjvf $dir/$1 -C $dir
	mongorestore --db "nordlys-v02" $dir
	rm -rf $dir
}

echo "############ Loading Mongo collection ..."
load_collection $1

# # ---
# # DBpedia 2015-10 collection
# echo "############ Loading dbpedia-2015-10 collection ..."
# load_collection mongo_dbpedia-2015-10.tar.bz2
#
#
# # ---
# # DBpedia surface forms collection
# echo "############ Loading surface_forms_dbpedia collection ..."
# load_collection mongo_surface_forms_dbpedia.tar.bz2
#
# # ---
# # DBpedia surface forms collection
# echo "############ Loading surface_forms_facc collection ..."
# load_collection mongo_surface_forms_facc.tar.bz2
#
# # ---
# # Freebase to DBpedia collection
# echo "############ Loading fb2dbp-2015-10 collection ..."
# load_collection mongo_fb2dbp-2015-10.tar.bz2
#
# # ---
# # Freebase to DBpedia collection
# echo "############ Loading word2vec-googlenews collection ..."
# load_collection mongo_word2vec-googlenews.tar.bz2
