# Check whether MongoDB is running or not.
mongo --eval "db.stats()"
RESULT=$?
if [ $RESULT -ne 0 ]; then
    echo "MongoDB is not running!"
    exit 1
else
    echo "MongoDB is running."
fi

load_collection () {
	mkdir -p $(pwd)/tmp
	dir=$(pwd)/tmp
	wget https://iai.group/downloads/nordlys-v02/$1 -P $dir
	tar -xjvf $dir/$1 -C $dir
	mongorestore --db "nordlys-v02" $dir
	rm -rf $dir
}

echo "Loading MongoDB collection $1 ..."
load_collection $1
