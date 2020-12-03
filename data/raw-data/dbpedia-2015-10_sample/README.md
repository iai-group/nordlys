# DBpedia 2015-10 sample

This directory contains a sample of the DBpedia 2015-10 collection, which can be used for testing a Nordlys installation.

To use the sample instead of the full collection, change the path in the `data/config/dbpedia-2015-10/dbpedia2mongo.config.json` file to load the data files to MongoDB (and then run indexing). Note that the sample is only sufficient for testing out some of the core functionality, i.e., building an entity index and performing entity retrieval. Additional functionality (entity linking, target type identification, etc.) relies on other data sources, which are not available in a sample form.

The sample was generated from a complete dump using the `nordlys.core.data.dbpedia.create_sample` module.