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
