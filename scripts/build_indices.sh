if [ $1 = 'dbpedia' ]
then
        echo "############ Building DBpedia index ..."
        python -m nordlys.core.data.dbpedia.indexer_dbpedia data/config/index_dbpedia_2015_10.config.json
elif [ $1 == 'types' ]
then
        echo "############ Building DBpedia types index ..."
        python -m nordlys.core.data.dbpedia.indexer_dbpedia_types data/config/index_dbpedia_2015_10_types.config.json
elif [ $1 == 'dbpedia_uri' ]
then
        echo "############ Building DBpedia URI-only index ..."
        python -m nordlys.core.data.dbpedia.indexer_dbpedia_uri data/config/index_dbpedia_2015_10_uri.config.json
fi
