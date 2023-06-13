# Redis & Python
*Notes & highlights from https://realpython.com/python-redis/*

### What is Redis?
Redis is an extremely fast, in-memory, key-value datastore that can be implemented as a caching system, a message queue, or a full on database.

- **in-memory** means that Redis data is not persistent. It only lasts while the process is running.

- **key-value** means that the data is stored as key-value pairs where the key is always a `string` data type while the value can be a different data type.

### Installation of Redis (from source)
**(Unix/MacOSX)**
```sh
$ redisurl="http://download.redis.io/redis-stable.tar.gz"
$ curl -s -o redis-stable.tar.gz $redisurl
$ sudo su root
$ mkdir -p /usr/local/lib/
$ chmod a+w /usr/local/lib/
$ tar -C /usr/local/lib/ -xzf redis-stable.tar.gz
$ rm redis-stable.tar.gz
$ cd /usr/local/lib/redis-stable/
$ make && make install
```

Check installation:
```sh
$ redis-cli --version
```

### Configuration
```sh
$ sudo su root
$ mkdir -p /etc/redis/
$ touch /etc/redis/6379.conf
```

Now write the following to /etc/redis/6379.conf (for a local development environment):
```Text
# /etc/redis/6379.conf

port              6379
daemonize         yes
save              60 1
bind              127.0.0.1
tcp-keepalive     300
dbfilename        dump.rdb
dir               ./
rdbcompression    yes
```

When using Redis in production, it helps to familiarise yourself with the official [sample `redis.conf` file](http://download.redis.io/redis-stable/redis.conf) and tune the settings to meet your needs.

### Running Redis
There are two utilities that are installed with the Redis installation. `redis-cli` and `redis-server`.

`redis-cli` allows us to interact with the Redis server in a REPL environment. Before doing that, one needs to start up the actual Redis server with `redis-server` like so:

```sh
$ redis-server /etc/redis/6379.conf
```

Since we set the `daemonize` config to `yes`, the above server will run in background. We can get the process ID by using `pgrep redis-server` - this will also confirm if the server is actually running. We can kill the process and stop the server by using `pkill redis-server`.




When you run just redis-cli from the command line, this starts you at database 0. Use the -n flag to start a new database, as in redis-cli -n 5.

The Redis() class has several parameters like host, port, and db. The db signifies the database ID. By default, the database with ID 0 is used. The max number of databases is 16.

redis-py requires that you pass it keys that are bytes, str, int, or float. (It will convert the last 3 of these types to bytes before sending them off to the server.)

Redis pipelining, which is a way to cut down the number of round-trip transactions that you need to write or read data from your Redis server. If you would have just called r.hmset() three times, then this would necessitate a back-and-forth round trip operation for each row written.

With a pipeline, all the commands are buffered on the client side and then sent at once, in one fell swoop.
