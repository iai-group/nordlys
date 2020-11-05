# DBpedia 2015-10 collection

This directory contains the core DBpedia 2015-10 sample files used by Nordlys. 

The directory, by default, contains  a minimal sample from DBpedia 2015-10, which can be used for testing Nordlys on a local machine.

By running the *DBpedia 2015-10 collection* block of `scripts/download_all.sh` script, the original DBpedia files will be downloaded.

## Getting the files

Run the *Type-to-entity mapping sample*  and *Freebase to DBpedia sample*  blocks of `scripts/download_all.sh` script from the `nordlys-v02` directory to download the needed files to build the indices.

Alternatively, you can run:

```
./scripts/download_all.sh
```

from the `nordlys-v02` directory. This will download all data raw files needed for Nordlys for both the sample DBpedia collection and the original DBpedia collection.


