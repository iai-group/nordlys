Processing FACC1
================

This folder contains scripts for extracting (name variant, Freebase entity, count) triples from the Freebase-Annotated Clueweb Collection (FACC1).

(http://lemurproject.org/clueweb09/FACC1/)

(http://lemurproject.org/clueweb12/FACC1/)

The original files come compressed (.tgz) in an 8-column format (including ClueWeb docids, encoding, and offsets). 
We only use the surface form (column 3) and linked Freebase entity (column 8) fields.

The output we generate is a set of files with name_variant, Freebase_entity, count tsv values.
Specifically, we generate a single file per subdirectory, but do not aggregate them further. (Aggregation is done in nordlys when inserting data into MongoDB.)


1. The `extract.sh` script takes care of the decompression and extraction of name_variant and Freebase_entity fields. 
It creates a single file for each annotated subdirectory (e.g., `ClueWeb12-FACC1/ClueWeb12_00/0000tw/` => `ClueWeb12-FACC1-extracted/ClueWeb12_00-0000tw.tsv`.)
The `INPUT` and `OUTPUT` variables in the beginning of the files need to be set manually.

2. The `counts.sh` script takes the output of `extract.sh` as input and aggregates the counts for (name variant, Freebase entity) pairs *per file*.
(E.g., `ClueWeb12-FACC1-extracted/ClueWeb12_00-0000tw.tsv` => `ClueWeb12-FACC1-counts/ClueWeb12_00-0000tw.tsv`)
The `extracted` dir may be deleted after this step has completed.


### Statistics

|                          | ClueWeb09 | ClueWeb12 |
|--------------------------|-----------|-----------|
| number of .tsv files     |       138 |       358 |
| size, extracted (\*.tsv) |       82G |      107G | 
| size, counts (\*.tsv)    |      5.3G |      7.2G | 


The size of the files (compressed) is about 2.4 GB.


## Getting the files

To download the compressed file `ClueWeb12-FACC1-counts.bz2` which contains files of the counts pairs for (name variant, Freebase entity), run the *FACC* block of `scripts/download_all.sh` script from the `nordlys-v02` directory. After the download is completed, the file has to be extracted. 


Alternatively from the `nordlys-v02` directory you can run:

```
./scripts/download_all.sh
```

This will download all data raw files needed for Nordlys.