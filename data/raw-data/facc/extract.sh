#!/bin/sh

# Input is the raw FACC data (all .tgz files in a single directory)
# - extract tgz files
# - keep only mention string and linked Freebase URL -- one tsv file per subdirectory
# - delete uncompressed files (but keep orig tgz-s)
#
# Set INPUT and OUTPUT variables before running the script!

INPUT=/home/krisztib/export/ClueWeb12-FACC1
OUTPUT=/home/krisztib/export/ClueWeb12-FACC1-extracted
TMPDIR=tmp-facc1

mkdir $OUTPUT
mkdir $TMPDIR

for tgzfile in `ls -1 $INPUT/*.tgz`
do
	echo $tgzfile
	tar -xzvf $tgzfile -C $TMPDIR
	
	cd $TMPDIR
	for split in `ls -1`
	do
		for d in `ls -1 $split/`
		do 
			cut -f3,8 $split/$d/*.tsv >$OUTPUT/$split-$d.tsv
		done
	done
	rm -rf *
	cd ..
done

rmdir $TMPDIR
