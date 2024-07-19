import logging
import os
import os.path
import uuid
import sys
import redis
import pandas as pd
import json
from datetime import datetime, timezone

"""
This script was made in the purpose of easily loading a .csv file listing
coordinates to a Redis Queue.
"""

def load_csv_to_redis_queue(filepath: str, r: redis.Redis):
    """
    load_csv_to_redis_queue read an .csv file listing coordinates
    and push them each row into a Redis queue.
    """
    try:
        df = pd.read_csv(filepath)
    except:
        logging.error(f"failed to read {filepath}")
        return

    nb_skipped_row: int = 0

    for idx, row in df.iterrows():
        try:
            # Select some of the row's columns to create a location dict.
            location = {
                'longitude': row['Longitude'],
                'latitude': row['Latitude'],
                'road_type': row['Road_Type'],
                'labels': {
                    'accident_index': str(row['Accident_Index']),
                    'pushing_id': f"{NAME}:{VERSION}:{SESSION_ID}",
                    'pushed_at': datetime.now(timezone.utc).astimezone().isoformat(),
                }
            }
        except:
            logging.warn(
                f"failed to parse location in row n°{idx} from {filepath}")

            nb_skipped_row += 1
            # Skip row
            continue

        # Convert the location to json to enable its pushing to the Redis queue.
        location_json = json.dumps(location)

        # Then push the location to the redis queue.
        try:
            r.rpush(REDIS_QUEUE_NAME, location_json)
        except:
            logging.error(
                f"failed to push element in Redis queue: \"{REDIS_QUEUE_NAME}\"")
            return

    if nb_skipped_row > 0:
        logging.warn(f"script completed loading and skipped {nb_skipped_row} in total from {filepath}")
    else:
        logging.info(f"script completed loading and didn't encountered with the {filepath}")


if __name__ == "__main__":
    # Set configuration variables from environment variables
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', '')
    REDIS_DB = int(os.environ.get('REDIS_DB', 0))
    REDIS_QUEUE_NAME = os.environ.get('REDIS_QUEUE_NAME', 'locations')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    SOURCE_FILEPATH = os.environ.get('SOURCE_FILEPATH', './locations.csv')
    NAME = 'dmml-pink-twins-pusher'
    VERSION = os.environ.get('VERSION', 'undefined')
    SESSION_ID = str(uuid.uuid4())

    # Set logger format
    logging.basicConfig(
        format="%(levelname)s | %(asctime)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
        encoding='utf-8',
        level=logging.getLevelName(LOG_LEVEL),
        stream=sys.stdout,
    )

    # Init Redis client
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    except:
        logging.error('failed to create Redis client')

    load_csv_to_redis_queue(SOURCE_FILEPATH, r)
