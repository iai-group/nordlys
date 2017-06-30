# --
# DBpedia
echo "############ Importing  DBpedia to MongoDB ..."
python -m nordlys.core.data.dbpedia.dbpedia2mongo data/config/dbpedia2mongo.config.json

# --
# DBpedia surface form
echo "############ Importing DBpedia surface form dictionary to MongoDB ..."
python -m nordlys.core.data.dbpedia.dbpedia_surfaceforms2mongo data/config/dbpedia_surfaceforms2mongo.config.json

# --
# FACC surface forms
echo "############ Importing FACC surface form dictionary to MongoDB ..."
python -m nordlys.core.data.facc.facc2mongo data/config/facc2mongo.config.json

# --
# Freebase to DBpedia mapping
echo "############ Importing Freebase to DBpedia mappings ..."
python -m nordlys.core.data.dbpedia.freebase2dbpedia2mongo  data/config/freebase2dbpedia2mongo.config.json

# --
# Word2Vec
echo "############ Importing Word2Vec (Google news-300D) ..."
python -m nordlys.core.data.word2vec.word2vec2mongo data/config/word2vec2mongo.config.json
