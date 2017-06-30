#!/bin/sh

# Input is the extracted mention strings and linked Freebase URLs (output of extract.sh)
# Output is (name variant, Freebase entity, count) triples tab separated (per file)
#
# Set INPUT and OUTPUT variables before running the script!

INPUT=/home/krisztib/export/ClueWeb12-FACC1-extracted
OUTPUT=/home/krisztib/export/ClueWeb12-FACC1-counts

mkdir $OUTPUT

for tsvfile in `ls -1 $INPUT/*.tsv`
do
	echo $tsvfile
	f=$(basename "$tsvfile")
	
	sort $tsvfile | uniq -c | sed -e 's/ *//' -e 's/ /\t/' | awk -F"\t" '{printf("%s\t%s\t%s\n",$2,$3,$1)}' >$OUTPUT/$f
done
