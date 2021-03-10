# Builds indices for a specific version of DBpedia:
# 2015-10 (default) or 2016-10 (if provided as 2nd argument)

if [ $# -eq 0 ]; then
  echo "Usage: build_dbpedia_index.sh index_type [2016-10]"
  echo ""
  echo "  - index_type is either core, types, or uri"
  echo "  - 2016-10 refers to the DBpedia version, to overwrite the default of 2015-10"
  exit 1
fi

# DBpedia version
VERSION=2015-10
if [ $2 = "2016-10" ]; then
  VERSION=2016-10
fi

if [ $1 = "core" ]
then
        echo "############ Building DBpedia $VERSION core index ..."
        python -m nordlys.core.data.dbpedia.indexer_dbpedia data/config/dbpedia-$VERSION/index.config.json
elif [ $1 = "types" ]
then
        echo "############ Building DBpedia $VERSION types index ..."
        python -m nordlys.core.data.dbpedia.indexer_dbpedia_types data/config/dbpedia-$VERSION/index_types.config.json
elif [ $1 = "uri" ]
then
        echo "############ Building DBpedia $VERSION URI-only index ..."
        python -m nordlys.core.data.dbpedia.indexer_dbpedia_uri data/config/dbpedia-$VERSION/index_uri.config.json
fi
