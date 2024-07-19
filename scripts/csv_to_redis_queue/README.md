# csv_to_redis_queue

## Overview
The following python scripts have been made in the purpose of easily
loading a list of coordinates stored as a .csv file to a Redis queue.

![The complete stack](../../data/img/dmml-pink-twins-satellite-images-loading.png)

## Getting Started

### Run with Docker

#### Requirements
To run this script you'll need the following:
- [docker](https://www.docker.com/get-started/)
- [docker compose](https://docs.docker.com/compose/install/)

#### Step by Step
1. Setup the containers with docker compose with the following command line:

```sh
docker compose up
```

2. Wait a couple of seconds for this log to appear in the console
```
csv_to_redis_queue-1 exited with code 0
```

And the Redis queue should be ready to be consummed at `localhost:6379`.

### Run locally

#### Requirements
To run the script locally you'll need:
- [python3.10.12](https://www.python.org/downloads/)
- [python3-pip](https://pip.pypa.io/en/stable/installation/#)
- a Redis server running

#### Step by Step
1. Install the dependencies of the script:
```sh
pip install -r requirements.txt
```

2. Then run the script (you'll maybe need to change a bit the environment variable if your Redis server doesn't run locally at port 6379 or does have a password check):
```sh
python3 main.py
```

### Configuration
You can configure the script with the following environment variables:

| NAME | DEFAULT VALUE | DESCRIPTION |
| :---: | :---: | :---: |
| REDIS_HOST | localhost | The host of the Redis server |
| REDIS_PORT | 6379 | The port at which the Redis server listen |
| REDIS_PASSWORD | - | The password to connect to the Redis server |
| REDIS_DB | 0 | The database to use in the Redis server |
| REDIS_QUEUE_NAME | locations | The name of the queue to push location at in the redis server |
| LOG_LEVEL | INFO | The minimum log type to output |
| SOURCE_FILEPATH | ./locations | The filepath of the file to load elements from to the Redis queue |
| ORIGIN_VERSION | undefined | The version of the script |
