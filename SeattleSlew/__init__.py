from datetime import datetime

# Create Cosmos Client and Authenticate
import os
import sys
from random import randint

import pymongo
from dotenv import load_dotenv

load_dotenv()
CONNECTION_STRING = os.environ.get("COSMOS_CONNECTION_STRING")

DB_NAME = "cytology"
COLLECTION_NAME = "samples"

client = pymongo.MongoClient(CONNECTION_STRING)

# Create database if it doesn't exist
db = client[DB_NAME]
if DB_NAME not in client.list_database_names():
    # Create a database with 400 RU throughput that can be shared across
    # the DB's collections
    db.command({"customAction": "CreateDatabase", "offerThroughput": 400})
    print("Created db '{}' with shared throughput.\n".format(DB_NAME))
else:
    print("Using database: '{}'.\n".format(DB_NAME))

# Create collection if it doesn't exist
collection = db[COLLECTION_NAME]
if COLLECTION_NAME not in db.list_collection_names():
    # Creates a unsharded collection that uses the DBs shared throughput
    db.command(
        {"customAction": "CreateCollection", "collection": COLLECTION_NAME}
    )
    print("Created collection '{}'.\n".format(COLLECTION_NAME))
else:
    print("Using collection: '{}'.\n".format(COLLECTION_NAME))

# Create an index 

# Create new document and upsert (create or replace) to collection
sample = {
    "patient_name": "John Doe",
    "sample_date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
}
result = collection.update_one(
    {"patient_name": sample["patient_name"]}, {"$set": sample}, upsert=True
)
print("Upserted document with _id {}\n".format(result.upserted_id))