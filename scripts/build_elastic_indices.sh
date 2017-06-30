# --
# DBpedia Types index
echo "############ Building DBpedia types index ..."
python -m nordlys.core.data.dbpedia.indexer_dbpedia_types data/config/index_dbpedia_2015_10_types.config.json

# --
# DBpedia URI-only index
echo "############ Importing DBpedia URI-only index ..."
python -m nordlys.core.data.dbpedia.indexer_dbpedia_uri data/config/index_dbpedia_2015_10_uri.config.json

